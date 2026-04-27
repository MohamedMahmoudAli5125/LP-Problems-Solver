import numpy as np
from .models import LPProblemModel, StandardizerOutput
class Standardizer:
    def __init__(self, model: LPProblemModel):
        self.model = model

    def standardize(self):
        unrestricted_count = sum(1 for v_type in self.model.var_types if v_type == "Unrestricted")
        decision_cols = self.model.num_vars + unrestricted_count
        # self.StandardOutput = StandardizerOutput()
        
        slack_cols = 0
        artificial_cols = 0
        # Count the number of slack and artificial variables needed based on the constraints (to determine the size of A and the objective vectors)
        for op in self.model.operators:
            if op == "≤":
                slack_cols += 1
            elif op == "≥":
                slack_cols += 1       
                artificial_cols += 1  
            elif op == "=":
                artificial_cols += 1 
   
        total_cols = decision_cols + slack_cols + artificial_cols
        num_constraints = len(self.model.constraints_matrix)
        
        #metadata to keep track of what each column in A represents (e.g., x1, x2, s1, a1, etc.) index will correspond to the column in A and the objective vectors. 
        #    This mapping will help us know which columns in A correspond to the original decision variables, especially since unrestricted variables will be split into two columns. It will be a list of tuples, where each tuple corresponds to an original variable and contains the indices of the columns in A that represent it (one or two columns depending on whether it's unrestricted).

        A = np.zeros((num_constraints, total_cols))
        b = np.array(self.model.rhs_list, dtype=float)
        phase1_obj = np.zeros(total_cols)
        phase2_obj = np.zeros(total_cols - artificial_cols)
        col_metaData = []  
        var_mapping = []
        
        
        current_col = 0
        for i in range(self.model.num_vars):
            if self.model.var_types[i] == "Unrestricted":
                
                col_metaData.append(f"x{i+1}+")
                col_metaData.append(f"x{i+1}-")
        
                var_mapping.append((current_col, current_col + 1))
        
                val = self.model.obj_coeffs[i]
                phase2_obj[current_col] = val 
                phase2_obj[current_col + 1] = -val

                current_col += 2
            else:         
              col_metaData.append(f"x{i+1}")
              var_mapping.append((current_col,))
        
              phase2_obj[current_col] = self.model.obj_coeffs[i]
              current_col += 1
            
        #slacks will be placed after the decision variable columns, and artificials will be placed after slacks. So we can keep track of where the slack and artificial columns start with two pointers: one for slacks and one for artificials.
        slack_start_idx = current_col
        art_start_idx = current_col + slack_cols

        current_slack_ptr = slack_start_idx
        current_art_ptr = art_start_idx

        for j in range(num_constraints):    
            row_coeffs = np.array(self.model.constraints_matrix[j])
            rhs = self.model.rhs_list[j]
            op = self.model.operators[j]
    
            if rhs < 0:      
                row_coeffs *= -1
                rhs *= -1
                if op == "≤": op = "≥"
                elif op == "≥": op = "≤"
    
                b[j] = rhs

            for i, cols in enumerate(var_mapping):              
                val = row_coeffs[i]
                if len(cols) == 2: 
                    
                    A[j, cols[0]] = val
                    A[j, cols[1]] = -val
                else: 
                    A[j, cols[0]] = val

            if op == "≤":          
                A[j, current_slack_ptr] = 1
                col_metaData.append( f"s{j+1}") 
                current_slack_ptr += 1
        
            elif op == "≥":
               A[j, current_slack_ptr] = -1 
               col_metaData.append( f"s{j+1}")
               current_slack_ptr += 1
        
               A[j, current_art_ptr] = 1   
               phase1_obj[current_art_ptr] = 1 # only artificial variables in phase 1 obj
               col_metaData.append( f"a{j+1}")
               current_art_ptr += 1
        
            elif op == "=":
               A[j, current_art_ptr] = 1   
               phase1_obj[current_art_ptr] = 1 # only artificial variables in phase 1 obj
               col_metaData.append( f"a{j+1}")
               current_art_ptr += 1
           
        #so to know what is the models now 
        # A is the tableu for phase 1 without the objective row, b is the rhs vector
        # phase1_obj is the objective coefficients for phase 1 (which will have 1s for artificial variables and 0s elsewhere),
        # and phase2_obj is the objective coefficients for phase 2 (which will have the original objective coefficients for the decision variables and 0s for slacks . 
        # The col_metaData list will help us understand which column corresponds to which variable in the standardized tableau.
        # objective type  
        # the determination of whether the obj coefficients will be made positive or negative will be handeled in another function in the solver depending on the objective type (max or min) , 
        # Standardizer's role is just to prepare the tableau data in a consistent format, and the solver will handle the logic of how to use that data based on the objective type.
        return StandardizerOutput(A, b, phase1_obj, phase2_obj, col_metaData, self.model.obj_type)
    
    
