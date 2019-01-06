import argparse
import json

import voicesep as vs

def separate(score, parameters, overrides):

    separators = []
    for separator in parameters["separators"]:
        name = next(iter(separator))
        args = separator[name]

        if overrides:
            override_args = override[name]

            for key, value in override_args.items():
                args[key] = value

        separators.append((name, args))

    beat_horizon = parameters["beat_horizon"]

    return vs.separate(score, separators, beat_horizon)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--parameters",
        type=str,
        required=True,
        help=""
    )

    args = parser.parse_args()

    with open(args.parameters) as fp:
        parameters = json.load(fp)

    scores_path = parameters["scores_path"]
    benchmark = parameters["benchmark"]
    actual = parameters["actual"]
    evaluations = parameters["evaluations"]

    evaluator = Evaluator()

    for score_file in scores_files:
        score = vs.Score(score_file)

        benchmark_assignments = separate(score, benchmark, overrides)
        actual_assignments = separate(score, actual, overrides)

        for pair_filter in pair_filters:
            evaluator.update(
                score,
                benchmark_assignments,
                actual_assignments,
                pair_filter
            )

    evaluator.write(results_file)


if __name__ == "__main__":
    main()
