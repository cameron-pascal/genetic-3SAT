import dimacs_parser


class Runner:

    def __init__(self, dimac_problems: list):

        self._formulas = []
        for problem in dimac_problems:
            formula = dimacs_parser.parse(problem)
            self._formulas.append(formula)

    def run(self):
        return

