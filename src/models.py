import numpy as np

class LPProblemModel:
    def __init__(self):
        self.num_vars = 0  
        self.obj_type = "Max"  
        self.obj_coeffs = []
        self.constraints_matrix = []  
        self.rhs_list = []  
        self.operators = []  
        self.var_types = []

class StandardTableau:
    def __init__(self, matrix, basis):
        self.tableau = np.array(matrix, dtype=float)  
        self.basis_indices = basis   
        self.status = "optimal"  
        self.obj_value = 0.0  
        
