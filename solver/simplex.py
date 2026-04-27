import numpy as np
from .utils import pivot

class SimplexSolver:
    def __init__(self, A, b, c):
        self.A = A  # Coefficient matrix
        self.b = b  # Right-hand side vector
        self.c = c  # Objective function coefficients
        self.objective_type = 'max'  # Type of optimization (max or min)
        self.constraints_type = [] # List to store the type of each constraint (<=, >=, =)
        self.status = None # Status of the solution (optimal, infeasible)
        self.steps = [] # Tableau at each iteration
        self.solution = {} # The optimal objective function value and variable values


    def solve(self):
        pass

    # Build the initial tableau for the standard simplex method
    def build_tableau(self):
        n_cons = len(self.b)
        n_vars = len(self.c)

        b = np.array(self.b).reshape(-1, 1)
        slacks = np.eye(n_cons)
        z_row = np.zeros((1, n_vars + n_cons + 1))

        z_row = np.hstack((-np.array(self.c), np.zeros(n_cons), np.array([0]))).reshape(1, -1)
        tableau = np.hstack((self.A, slacks, b))
        tableau = np.vstack((tableau, z_row))

        return tableau

    # Determination of the entering variable
    def get_entering_variable(self, tableau):
        entering_col = -1
        z_row = tableau[-1, :-1] # RHS excluded

        if self.objective_type == 'max':
            min_value = np.min(z_row)
            if min_value < 0:
                entering_col = np.argmin(z_row)
        else:
            max_value = np.max(z_row)
            if max_value > 0:
                entering_col = np.argmax(z_row)

        return entering_col

    # Determination of the leaving variable
    def get_leaving_variable(self, tableau, entering_col):
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
        

#test
# if __name__ == "__main__":
#     A = [[2, 1, 1], [1, 2, 3], [2, 2, 1]]
#     b = [2, 5, 6]
#     c = [3, 1, 3]

#     solver = SimplexSolver(A, b, c)
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
