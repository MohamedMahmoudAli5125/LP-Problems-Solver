class LPProblemModel:
    def __init__(self):
        self.num_variables = 0

    def set_num_vars(self, n):
        self.num_variables = n
        return self.num_variables