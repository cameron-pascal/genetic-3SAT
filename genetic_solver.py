import numpy as np
import cnf


class GeneticSolver:

    POPULATION_SIZE = 10
    MOTHER_CROSSOVER_PROB = 0.5
    FATHER_CROSSOVER_PROB = 0.5
    MUTATION_PROB = 0.9

    def __init__(self, formula: cnf.CnfFormula):
        self._formula = formula
        self._population = np.zeros((GeneticSolver.POPULATION_SIZE, formula.variable_count), np.bool)

        k = GeneticSolver.POPULATION_SIZE
        y = formula.variable_count

        # Let f(x) = x represent the number of true values in the range 0..variable_count
        # We discretize f into k uniform width partitions. Each partition corresponds to a specimen in the population
        # We use the truncated mid in a partition to set the initial number of true values in a corresponding specimen
        # This should give us a nice linear distribution of true and false values to begin.
        # Truncation error may be introduced
        for i in range(1, k+1):
            truth_count = int(((2 * i * y) - y) / (2 * k))

            for j in range(0, truth_count):
                self._population[i-1, j] = True

        # Here we are randomizing the distribution of variables
        # We transpose because shuffle only shuffles the first axis
        self._population.transpose()
        np.random.shuffle(self._population)
        self._population.transpose()

    def solve(self):
        return

