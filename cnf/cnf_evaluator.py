import numpy as np
import cnf


class CnfEvaluator:

    def __init__(self, formula: cnf.CnfFormula):
        self._formula = formula

    def evaluate(self, variable_instances: np.array):

        satisfied_clauses = np.zeros(self._formula.clause_count, np.bool)
        satisfied_count = 0

        it = np.nditer(self._formula.logical_matrix, flags=['multi_index'])
        while not it.finished:
            clause_idx = it.multi_index[0]

            if satisfied_clauses[clause_idx]:
                it.iternext()

            term_idx = it.multi_index[1]

            variable = self._formula.logical_matrix[clause_idx, term_idx]

            truth_value = variable_instances[variable - 1]

            if variable < 0:
                truth_value = not truth_value

            if truth_value:
                satisfied_count += 1
                satisfied_clauses[clause_idx] = True

            it.iternext()

        return satisfied_count


