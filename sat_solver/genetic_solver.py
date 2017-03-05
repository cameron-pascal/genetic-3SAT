import cnf


class GeneticSolver:

    MOTHER_CROSSOVER_PROB = 0.5
    FATHER_CROSSOVER_PROB = 0.5
    MUTATION_PROB = 0.9

    def __init__(self, formula: cnf.CnfFormula):
        self._formula = formula