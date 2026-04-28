import numpy as np

from .standardizer import Standardizer
from .utils import pivot
from .models import LPProblemModel, StandardizerOutput

class SimplexSolver:
    def __init__(self, model: LPProblemModel, std_output: StandardizerOutput):
        self.model = model
        self.std_output = std_output
        self.status = None # Status of the solution (optimal, infeasible)
        self.steps = [] # Tableau at each iteration
        self.solution = {} # The optimal objective function value and variable values


    def solve(self):
        has_artificials = np.any(self.std_output.phase1_obj == 1)
        tableau, basis = self._build_tableau(has_artificials)
        self.steps.append(tableau.copy())

        if has_artificials:
            tableau, basis = self._run_phase1(tableau, basis)
            if self.status == "infeasible":
                return
            
            tableau, basis = self._transition_to_phase2(tableau, basis)

        self._run_phase2(tableau, basis)
            
        #solution
        if self.status =="Optimal":
            output_value = tableau[-1,-1]
            if self.model.obj_type.lower() =="max":
                output_value =-output_value
            self.solution["objective_value"] = float(output_value)
            
            if has_artificials:
                art_indices = np.where(self.std_output.phase1_obj == 1)[0]
                final_metadata = [m for i , m in enumerate(self.std_output.col_metaData) if i not in art_indices]
            else:
                final_metadata=self.std_output.col_metaData
                
            for c , var_name in enumerate(final_metadata):
                if np.count_nonzero(tableau[:-1,c]) == 1 and np.max(tableau[:-1,c]) == 1:
                    row = np.where(tableau[:-1,c] == 1)[0][0]
                    self.solution[var_name] = float(tableau[row,-1])
                else:
                    self.solution[var_name] = 0.0
                    
            for i in range(self.model.num_vars):
                if self.model.var_types[i] =="Unrestricted":
                    pos_val = self.solution.get(f"x{i+1}+",0)
                    neg_val = self.solution.get(f"x{i+1}-",0)
                    self.solution[f"x{i+1}"] = float(pos_val - neg_val)

    def _run_phase1(self, tableau, basis):
        tableau = self._setup_objective(tableau, basis)
        self.steps.append(tableau.copy())
        
        # run simplex iterations for phase 1
        while True:
            entering_column =self._get_entering_variable(tableau)
            if entering_column == -1:
                break
            
            leaving_row = self._get_leaving_variable(tableau, entering_column)
            if leaving_row == -1:
                self.status = "infeasible"
                return
            
            tableau = pivot(tableau, leaving_row, entering_column)
            basis[leaving_row] = entering_column

            self.steps.append(np.round(tableau.copy(), decimals=10))
            
        # feasibility check 
        if abs(tableau[-1][-1])>1e-5:
            self.status = "infeasible"
            return
        
        return tableau, basis
    
    def _transition_to_phase2(self, tableau, basis):
        art_indices = np.where(self.std_output.phase1_obj == 1)[0]

        # remove the bottom row
        tableau = tableau[:-1,:]

        # remove the artificial columns
        tableau = np.delete(tableau,art_indices,axis=1)

        # append real objective row
        c = np.array(self.std_output.phase2_obj, dtype=float)
        z_row = np.hstack((-c, np.zeros(1)))
        tableau = np.vstack((tableau, z_row))

        tableau = self._setup_objective(tableau, basis)
        self.steps.append(tableau.copy())

        return tableau, basis

    def _run_phase2(self, tableau, basis):
        self.steps.append(tableau.copy())

        while True:
            entering_column = self._get_entering_variable(tableau)
            if entering_column == -1:
                self.status = "Optimal"
                break
            
            leaving_row = self._get_leaving_variable(tableau,entering_column)
            if leaving_row == -1:
                self.status = "Unbounded"
                return 
            
            tableau = pivot (tableau,leaving_row,entering_column)
            basis[leaving_row] = entering_column

            self.steps.append(np.round(tableau.copy(), decimals=10))


    # Build the initial tableau for the standard simplex method
    def _build_tableau(self, has_artificials):
        A = np.array(self.std_output.A, dtype=float)
        b = np.array(self.std_output.b, dtype=float).reshape(-1, 1)

        if has_artificials:
            c = np.array(self.std_output.phase1_obj, dtype=float)
        else:
            c = np.array(self.std_output.phase2_obj, dtype=float)

        z_row = np.hstack((-c, np.zeros(1)))
        tableau = np.hstack((A, b))
        tableau = np.vstack((tableau, z_row))
        basis   = list(self.std_output.initial_basis)

        return tableau, basis

    # Determination of the entering variable
    def _get_entering_variable(self, tableau):
        objective_type = self.model.obj_type.lower()
        entering_col = -1
        z_row = tableau[-1, :-1] # RHS excluded

        if objective_type == 'max':
            min_value = np.min(z_row)
            if min_value < 0:
                entering_col = np.argmin(z_row)
        else:
            max_value = np.max(z_row)
            if max_value > 0:
                entering_col = np.argmax(z_row)

        return entering_col

    # Determination of the leaving variable
    def _get_leaving_variable(self, tableau, entering_col):
        min_ratio = float('inf')
        leaving_row = -1

        for r in range(len(tableau) - 1):  # Exclude the last row (objective function)
            if (tableau[r][entering_col] > 0):
                ratio = tableau[r][-1] / tableau[r][entering_col]
                if ratio < min_ratio:
                    #print(f"Row {r}: ratio = {ratio}")
                    min_ratio = ratio
                    leaving_row = r

        return leaving_row
    
    # clear basic variables from Z row
    def _setup_objective(self, tableau, basis):
        for row, col in enumerate(basis):
            multiplier = tableau[-1, col]
            if multiplier != 0:
                tableau[-1] -= multiplier * tableau[row]
        return tableau
        

#test
# if __name__ == "__main__":
#     A = [[2, 1, 1], [1, 2, 3], [2, 2, 1]]
#     b = [2, 5, 6]
#     c = [3, 1, 3]

#     model = LPProblemModel()
#     model.num_vars = 3
#     model.obj_type = "Max"
#     model.obj_coeffs = c
#     model.constraints_matrix = A
#     model.rhs_list = b

#     solver = SimplexSolver(model)
#     tableau = solver.build_tableau()

#     print("Tableau:")
#     print(tableau)

#     while True:
#         entering_col = solver.get_entering_variable(tableau)
#         # print(f"Entering variable column: {entering_col}")
#         if entering_col == -1:
#             break

#         leaving_row = solver.get_leaving_variable(tableau, entering_col)
#         # print(f"Leaving variable row: {leaving_row}")
#         if leaving_row == -1:
#             print("infeasible")
#             break

#         tableau = pivot(tableau, leaving_row, entering_col)

#     print("Optimal tableau:")
#     print(tableau)


# test



# if __name__ == "__main__":
#     model = LPProblemModel()
# # test the following problem:
# #     minimize − 3x1 + x2 + 3x3 − x4
# # subject to x1 + 2x2 − x3 + x4 = 0
# # 2x1 − 2x2 + 3x3 + 3x4 = 9
# # x1 − x2 + 2x3 − x4 = 6
# # xi ≥ 0, i = 1, 2, 3, 4.

#     #
#     model.num_vars = 4
#     model.obj_type = "min"
#     model.obj_coeffs = [-3, 1, 3, -1]
#     model.constraints_matrix = [[1, 2, -1, 1], [2, -2, 3, 3], [1, -1, 2, -1]]
#     model.rhs_list = [0, 9, 6]
#     model.operators = ["=", "=", "="]
#     model.var_types = ["Non-negative", "Non-negative", "Non-negative", "Non-negative"]

#     standardizer = Standardizer(model)
#     std_output = standardizer.standardize()




#     # print("A:\n", std_output.A)
#     # print("b:\n", std_output.b)
#     # print("Phase 1 Objective Coefficients:\n", std_output.phase1_obj)
#     # print("Phase 2 Objective Coefficients:\n", std_output.phase2_obj)
#     # print("Column Metadata:\n", std_output.col_metaData)

#     solver = SimplexSolver(model, std_output)
#     solver.solve()
#     # tableau, basis = solver.build_tableau(has_artificials = True)
#     # print("Initial Tableau:")
#     # print(tableau)

#     print("Status:", solver.status)
#     print("Optimal Solution:", solver.solution)

#     print("steps:")
#     for i, step in enumerate(solver.steps):
#         print(f"Step {i + 1}:")
#         print(step)