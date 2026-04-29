import numpy as np

from .standardizer import Standardizer
from .utils import pivot
from .models import LPProblemModel, StandardizerOutput

class SimplexSolver:
    def __init__(self, model: LPProblemModel, std_output: StandardizerOutput):
        self.model = model
        self.std_output = std_output
        self.status = None          # Status of the solution (optimal, infeasible)
        self.steps = []             # Tableau at each iteration
        self.step_labels = []       # Human-readable label per step (parallel to self.steps)
        self.step_basis = []
        self.solution = {}          # The optimal objective function value and variable values

    def _log(self, tableau: np.ndarray, label: str , basis: list) -> None:
        self.steps.append(tableau.copy())
        self.step_labels.append(label)
        self.step_basis.append(basis.copy())

    def solve(self):
        has_artificials = np.any(self.std_output.phase1_obj == 1)
        tableau, basis = self._build_tableau(has_artificials)
        if has_artificials:
            self._log(tableau, "Phase 1 – Initial Tableau (before objective setup)", basis)
        else:
            self._log(tableau, "Phase 2 – Initial Tableau", basis)

        if has_artificials:
            tableau, basis = self._run_phase1(tableau, basis)
            if self.status == "infeasible":
                return

            tableau, basis = self._transition_to_phase2(tableau, basis)

        tableau, basis = self._run_phase2(tableau, basis)
        #solution
        if self.status =="Optimal":
            output_value = tableau[-1,-1]
            #if self.model.obj_type.lower() =="max":
            #    output_value =-output_value
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
        self._log(tableau, "Phase 1 – After Objective Row Setup", basis)
        phase1 = True
        # run simplex iterations for phase 1
        iteration = 1
        while True:
            entering_column = self._get_entering_variable(tableau , phase1) # forcing the min approach in phase 1
            if entering_column == -1:
                break

            leaving_row = self._get_leaving_variable(tableau, entering_column)
            if leaving_row == -1:
                self.status = "infeasible"
                self._log(tableau, f"Phase 1 – Iteration {iteration} – INFEASIBLE (no leaving row)", basis)
                break
            leave_name = self._col_name(basis[leaving_row])

            tableau = pivot(tableau, leaving_row, entering_column)
            basis[leaving_row] = entering_column
            tableau = np.round(tableau, decimals=10)

            col_name = self._col_name(entering_column)
            self._log(tableau, f"Phase 1 – Iteration {iteration} – Enter: {col_name}, Leave: {leave_name}", basis)
            iteration += 1

        # feasibility check
        if abs(tableau[-1][-1])>1e-5:
            self.status = "infeasible"
            self._log(tableau, "Phase 1 – INFEASIBLE (artificial variable remains > 0)", basis)
        else:
            self._log(tableau, "Phase 1 – Complete (feasible BFS found)", basis)
            
        return tableau, basis

    def _transition_to_phase2(self, tableau, basis):
        art_indices = np.where(self.std_output.phase1_obj == 1)[0]
        
        # remove the bottom row
        tableau = tableau[:-1,:]                       
        # remove the artificial columns
        tableau = np.delete(tableau,art_indices,axis=1)  # drop artificial columns
        
        # append real objective row 
        c = np.array(self.std_output.phase2_obj, dtype=float)
        z_row = np.hstack((-c, np.zeros(1)))
        tableau = np.vstack((tableau, z_row))
        self._log(tableau, "Phase 2 – Initial Tableau (after dropping artificials)", basis)

        tableau = self._setup_objective(tableau, basis)
        self._log(tableau, "Phase 2 – Initial Tableau (after objective setup)", basis)
        return tableau, basis

    def _run_phase2(self, tableau, basis):
       # self.steps.append(tableau.copy())
        if not self.steps or "Phase 2" not in self.step_labels[-1]:
            self._log(tableau, "Phase 2 – Initial Tableau", basis)

        iteration = 1
        while True:
            entering_column = self._get_entering_variable(tableau , phase1=False)
            if entering_column == -1:
                self.status = "Optimal"
                self._log(tableau, f"Phase 2 – Optimal Solution Reached", basis)
                break

            leaving_row = self._get_leaving_variable(tableau,entering_column)
            if leaving_row == -1:
                self.status = "Unbounded"
                self._log(tableau, f"Phase 2 – Iteration {iteration} – UNBOUNDED (no leaving row)", basis)
                break
            leave_name = self._col_name(basis[leaving_row])

            tableau = pivot(tableau, leaving_row, entering_column)
            basis[leaving_row] = entering_column
            tableau = np.round(tableau, decimals=10)

            col_name = self._col_name(entering_column)
            self._log(tableau, f"Phase 2 – Iteration {iteration} – Enter: {col_name}, Leave: {leave_name}", basis)
            iteration += 1

        return tableau, basis

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
    def _get_entering_variable(self, tableau, phase1):
        z_row = tableau[-1, :-1]
        if phase1:
            objective_type = "min"  
        else:
            objective_type = self.model.obj_type.lower()

        if objective_type == 'max':
            min_val = np.min(z_row)
            return int(np.argmin(z_row)) if min_val < 0 else -1
        else:
            max_val = np.max(z_row)
            return int(np.argmax(z_row)) if max_val > 0 else -1
        
    # Determination of the leaving variable
    def _get_leaving_variable(self, tableau, entering_col):
        min_ratio  = float('inf')
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

    def _col_name(self, col_index: int) -> str:
        meta = self.std_output.col_metaData
        if col_index < len(meta):
            return meta[col_index]
        return f"col{col_index}"