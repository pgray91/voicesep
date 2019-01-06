import argparse
import json
import logging

import voicesep as vs


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

    for score_file in parameters["scores_path"]:
        score = vs.Score(score_file)

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


        assignments = vs.separate(score, separators, beat_horizon)
        score.write(output, assignments)


if __name__ == "__main__":
    main()
