import numpy as np


class CnfFormula:

    def __init__(self, logical_matrix: np.ndarray, variable_count: int, clause_count: int):
        self.logical_matrix = logical_matrix
        self.variable_count = variable_count
        self.clause_count = clause_count
