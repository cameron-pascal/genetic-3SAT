import os
import sys
import problem_runner


def main(argv):
    if len(argv) != 2:
        print("Invalid usage.")
        return 0

    path = argv[1]

    if not(os.path.isdir(path)):
        print("Specified directory does not exist")
        return 0

    problems = load_problem_set(path)

    runner = problem_runner.Runner(problems)

    runner.run()


def load_problem_set(path):
    problems = []

    for file in os.listdir(path):
        if file.endswith('.cnf'):
            f = open(os.path.join(path, file))
            problems.append(f.read())
            f.close()

    return problems


if __name__ == "__main__":
    main(sys.argv)
