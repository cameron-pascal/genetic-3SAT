import numpy as np
import re
import cnf


def parse(dimacs_data: str):

    lines = dimacs_data.split('\n')
    line_offset = 0

    for line in lines:
        if line[0] == 'c':
            line_offset += 1
            continue

        if line[0] == 'p':
            preamble = line.strip(' ')
            preamble = re.sub(' +', ' ', preamble)
            preamble = preamble.split(' ')
            variable_count = int(preamble[2])
            clause_count = int(preamble[3])
            lines_with_clauses = lines[line_offset + 1:]
            logical_matrix = __parse_clauses(lines_with_clauses, clause_count)
            return cnf.CnfFormula(logical_matrix, variable_count)


def __parse_clauses(lines_with_clauses: list, clause_count: int):

    # We are representing a 3CNF formula as a matrix where each vector is a clause
    logical_formula_matrix = np.zeros((clause_count, 3), np.int8)

    joined_lines = ''.join(lines_with_clauses)
    joined_lines = joined_lines.replace('0%0', '')
    clauses = re.split('[\t\n ]0|[\t\n ]0', joined_lines)

    for clause_index, clause in enumerate(clauses):
        clause = clause.strip(' ')
        variables_in_clause = re.split('[\t\n ]', clause)

        for term_index, variable in enumerate(variables_in_clause):
            numeric_representation = int(variable)
            logical_formula_matrix[clause_index, term_index] = numeric_representation

    print(logical_formula_matrix)
    print('\n')
    return logical_formula_matrix

