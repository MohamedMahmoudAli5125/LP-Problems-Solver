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

# class StandardTableau:
#     def __init__(self, matrix, basis):
#         self.tableau = np.array(matrix, dtype=float)  
#         self.basis_indices = basis   
#         self.status = "optimal"  
#         self.obj_value = 0.0  
#input to solver function will be an instance of this class, which will contain the standardized tableau data for both phases (with small changes for phase 2 if phase 1 succeeds). 
class StandardizerOutput:
    def __init__(self, A, b, phase1_obj , phase2_obj, col_metaData , objetive):
        self.A = A
        self.b = b
        self.phase1_obj = phase1_obj
        self.phase2_obj = phase2_obj
        self.col_metaData = col_metaData
        self.objetive = objetive