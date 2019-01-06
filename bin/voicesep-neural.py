import argparse
import json
import logging

import voicesep as vs

# args
# ----------
# dataset
# train
# neural
#   note_level
#   chord_level

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


    dimensions = parameters["dimensions"]
    hidden_activations = parameters["hidden_activations"]
    output_activations = parameters["output_activations"]

    network = vs.separators.neural.note_level.Network()

    network.build(dimensions, hidden_activations, output_activations)

    cost = parameters["cost"]
    L2_reg = parameters["L2_reg"]
    gradient_type = parameters["gradient_type"]
    gradient_args = parameters["gradient_args"]

    network.compile(cost, L2_reg, gradient_type, gradient_args)

    for score_file in parameters["scores_path"]:
        score = vs.Score(score_file)

        dataset = None

        beat_horizon = parameters["beat_horizon"]


        assignments = vs.separate(score, separators, beat_horizon)
        score.write(output, assignments)


if __name__ == "__main__":
    main()
