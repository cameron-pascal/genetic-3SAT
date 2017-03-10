import os
import sys
import problem_runner
import json
from json import JSONEncoder


class _Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

TIME_LIMIT = 36000  # 10 hours

def main(argv):
    if len(argv) != 3:
        print("Invalid usage.")
        return 0

    in_path = argv[1]
    out_path = argv[2]

    if not(os.path.isdir(in_path), os.path.isdir(out_path)):
        print("Specified directory does not exist")
        return 0

    problems = load_problem_set(in_path)

    runner = problem_runner.Runner(problems, out_path, TIME_LIMIT)

    data = runner.run()

    with open(os.path.join(out_path, "3sat_agg_data.json"), 'w') as out_file:
        json.dump(data, out_file, indent=4, cls=_Encoder)


def load_problem_set(path):
    problems = []

    for file in os.listdir(path):
        if file.endswith('.cnf'):
            with open(os.path.join(path, file)) as cnf_file:
                problems.append(cnf_file.read())

    return problems


if __name__ == "__main__":
    main(sys.argv)
