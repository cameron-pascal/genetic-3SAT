import dimacs_parser
import genetic_solver
import json
import os
import time
from json import JSONEncoder


class _Metrics:

    def __init__(self, variable_count):
        self.variable_count = variable_count
        self.success_count = 0
        self.failure_count = 0
        self.run_times = []
        self.bit_flips = []


class _Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class _AggregateStatistics:

    def __init__(self):
        self.median_run_time = 0
        self.success_rate = 0
        self.average_bit_flips = 0


class Runner:

    def __init__(self, dimacs_problems, data_dir, time_limit):

        self.time_limit = time_limit
        self.metrics_dir = os.path.join(data_dir, 'metrics')

        if not os.path.exists(self.metrics_dir):
            os.makedirs(self.metrics_dir)

        self._formulas = []
        for problem in dimacs_problems:
            formula = dimacs_parser.parse(problem)
            self._formulas.append(formula)

    def run(self):
        metrics_dict = {}
        variable_count_min = 0
        variable_count_max = 0

        time_remaining = self.time_limit
        count = 0
        for formula in self._formulas:

            remaining_problems = len(self._formulas) - count
            time_for_problem = time_remaining / remaining_problems

            solver = genetic_solver.GeneticSolver(formula, time_for_problem)

            time_start = time.time()
            solution = solver.solve()
            time_elapsed = time.time() - time_start

            time_remaining -= time_elapsed

            variable_count = formula.variable_count

            variable_count_max = max(variable_count, variable_count_max)
            variable_count_min = min(variable_count, variable_count_min)

            if variable_count in metrics_dict:
                metrics = metrics_dict[variable_count]
            else:
                metrics = _Metrics(variable_count)
                metrics_dict[variable_count] = metrics

            if solution is not None:
                metrics.success_count += 1
                metrics.bit_flips.append(solver.flip_count)
                metrics.run_times.append(solver.run_time)
            else:
                metrics.failure_count += 1

            count += 1
            with open(os.path.join(self.metrics_dir, "metrics_" + str(count) + '.json'), 'w') as out_file:
                json.dump(metrics, out_file, indent=4, cls=_Encoder)

            if time_remaining <= 0:
                break

        return self.__aggregate_data(metrics_dict)

    @staticmethod
    def __aggregate_data(metrics_dict):

        aggregate_data = {}

        for variable_count in metrics_dict.keys():
            metrics = metrics_dict[variable_count]

            statistics = _AggregateStatistics()

            if len(metrics.bit_flips):
                statistics.average_bit_flips = sum(metrics.bit_flips) / len(metrics.bit_flips)

            total_experiments = metrics.success_count + metrics.failure_count

            if total_experiments:
                statistics.success_rate = metrics.success_count / (metrics.success_count + metrics.failure_count)

            if len(metrics.run_times):
                metrics.run_times.sort()
                length = len(metrics.run_times)
                middle_index = (length - 1) // 2

                if length % 2 == 0:
                    a = metrics.run_times[middle_index - 1]
                    b = metrics.run_times[middle_index]
                    statistics.median_run_time = (a + b) / 2
                else:
                    statistics.median_run_time = metrics.run_times[middle_index]

            aggregate_data[variable_count] = statistics

        return aggregate_data
