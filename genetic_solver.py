import numpy as np
import cnf
import random
import time


class _EvaluationResult:
    def __init__(self, fitness, specimen_index):
        self.fitness = fitness
        self.specimen_index = specimen_index


class GeneticSolver:

    POPULATION_SIZE = 10
    ELITE_PROPAGATION_LIMIT = 2
    REPRODUCTION_POOL_SIZE = POPULATION_SIZE - ELITE_PROPAGATION_LIMIT  # Make sure this is an even number

    def __init__(self, formula: cnf.CnfFormula, time_limit):
        self.evaluator = cnf.CnfEvaluator(formula)
        self._formula = formula
        self.time_start = 0
        self.time_limit = time_limit
        self._population = np.zeros((GeneticSolver.POPULATION_SIZE, formula.variable_count), np.bool)
        self.flip_count = 0
        self.run_time = 0.0

        k = GeneticSolver.POPULATION_SIZE
        y = formula.variable_count

        # Let f(x) = x represent the number of true values in the range 0..variable_count
        # We discretize f into k uniform width partitions. Each partition corresponds to a specimen in the population
        # We use the truncated mid in a partition to set the initial number of true values in a corresponding specimen
        # This should give us a nice linear distribution of true and false values to begin.
        # Truncation error may be introduced
        for i in range(1, k + 1):
            truth_count = int(((2 * i * y) - y) / (2 * k))

            for j in range(0, truth_count):
                self._population[i - 1, j] = True

        # Here we are randomizing the distribution of starting variables
        # We transpose because shuffle only shuffles the first axis
        self._population.transpose()
        np.random.shuffle(self._population)
        self._population.transpose()

    def solve(self):

        self.time_start = time.time()

        population_results = []
        while True:

            if self.__is_time_up():
                return None

            for i in range(0, GeneticSolver.POPULATION_SIZE):

                if self.__is_time_up():
                    return None

                specimen = self._population[i, :]

                fitness = self.evaluator.evaluate(specimen)
                if fitness == self._formula.clause_count:
                    self.run_time = time.time() - self.time_start
                    return specimen

                result = _EvaluationResult(fitness, i)
                population_results.append(result)

            population_results.sort(key=lambda res: res.fitness, reverse=True)

            if not self.__generate_next_generation(population_results):
                return None

    def __generate_next_generation(self, population_results):

        fitness_sum = sum(r.fitness for r in population_results[GeneticSolver.ELITE_PROPAGATION_LIMIT:])
        reproduction_pool = []

        for _ in range(GeneticSolver.ELITE_PROPAGATION_LIMIT, GeneticSolver.POPULATION_SIZE):

            if self.__is_time_up():
                return False

            selected_index = self.__select_specimen(population_results, fitness_sum)
            reproduction_pool.append(selected_index)

        for i in range(GeneticSolver.ELITE_PROPAGATION_LIMIT, GeneticSolver.POPULATION_SIZE-1):

            if self.__is_time_up():
                return False

            should_mutate = random.random() >= 0.9

            for j in range(0, self._formula.variable_count):

                if self.__is_time_up():
                    return False

                should_flip = random.getrandbits(1)
                if random.getrandbits(1):
                    parent_index = reproduction_pool[i - GeneticSolver.ELITE_PROPAGATION_LIMIT]
                    self._population[i, j] = self._population[parent_index, j]
                else:
                    parent_index = reproduction_pool[i + 1 - GeneticSolver.ELITE_PROPAGATION_LIMIT]
                    self._population[i, j] = self._population[parent_index, j]

                if should_mutate & should_flip:
                    self.flip_count += 1
                    self._population[i, j] = not self._population[i, j]

            if not self.__perform_flip_heuristic(i):
                return False

            return True

    def __perform_flip_heuristic(self, population_index):

        initial_fitness = self.evaluator.evaluate(self._population[population_index, :])
        final_fitness = initial_fitness

        while True:
            order = np.arange(self._formula.variable_count)
            np.random.shuffle(order)
            for index in order:

                if self.__is_time_up():
                    return False

                pre_flip_fitness = self.evaluator.evaluate(self._population[population_index, :])
                self._population[population_index, index] = not self._population[population_index, index]
                final_fitness = self.evaluator.evaluate(self._population[population_index, :])

                gain = final_fitness - pre_flip_fitness

                if gain < 0:
                    self._population[population_index, index] = not self._population[population_index, index]
                else:
                    self.flip_count += 1

            if final_fitness <= initial_fitness:
                return True

            initial_fitness = final_fitness

    def __is_time_up(self):
        return time.time() - self.time_start > self.time_limit

    @staticmethod
    def __select_specimen(population_results, fitness_sum):
        selection_prob = random.random()
        cumulative_prob = 0.0
        for result in population_results[GeneticSolver.ELITE_PROPAGATION_LIMIT:]:
            cumulative_prob += result.fitness / fitness_sum
            if selection_prob <= cumulative_prob:
                return result.specimen_index
