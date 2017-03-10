import numpy as np
import cnf


class CnfEvaluator:

    def __init__(self, formula: cnf.CnfFormula):
        self._formula = formula

    def evaluate(self, variable_instances: np.array):

        satisfied_count = 0

        for clause_idx in range(0, self._formula.clause_count):
            for term_idx in range(0, 3):

                variable = self._formula.logical_matrix[clause_idx, term_idx]
                truth_value = variable_instances[abs(variable) - 1]

                if variable < 0:
                    truth_value = not truth_value

                if truth_value:
                    satisfied_count += 1
                    break

        return satisfied_count
