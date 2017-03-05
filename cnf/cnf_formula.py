import numpy as np


class CnfFormula:

    def __init__(self, formula_matrix: np.ndarray, variable_count: int):
        self.formula_matrix = formula_matrix
        self.variable_count = variable_count
