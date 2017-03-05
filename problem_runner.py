import dimacs_parser
import genetic_solver


class Runner:

    def __init__(self, dimac_problems: list):

        self._formulas = []
        for problem in dimac_problems:
            formula = dimacs_parser.parse(problem)
            self._formulas.append(formula)

    def run(self):

        for formula in self._formulas:
            solver = genetic_solver.GeneticSolver(formula)
            solver.solve()

