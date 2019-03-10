import logging


class ChordLevel(Separator):

    def __init__(
        self,
        score,
        network,
        convergence_limit=None,
        divergence_limit=None,
        assignments=""
    ):

        super().__init__(score)

        self.network = Network().open(network)

        dimensions = self.network.dimensions
        self.depths = dimensions[i][2] 

        self.convergence_limit = convergence_limit
        self.divergence_limit = divergence_limit

        self.assignments = Assignments(assignments)

    def run(self, chord, active_voices, assignment):

        max_assignment = None
        max_rank = 0
        pair_depth, convergence_depth, divergence_depth = self.depths

        features = Features(chord, active_voices)

        assignment_generator = assignments.generate(
            chord,
            active_voices,
            assignment,
            self.convergence_limit,
            self.divergence_limit
        )
        for predicted_assignment in assignment_generator:

            pair_data = features.pair_data(predicted_assignment)
            Features.pad(pair_data, pair_depth)

            convergence_data = features.convergence_data(predicted_assignment)
            Features.pad(convergence_data, convergence_depth)

            divergence_data = features.divergence_data(predicted_assignment)
            Features.pad(divergence_data, divergence_depth)

            assignment_data = features.assignment_data(predicted_assignment)

            rank = network.predict(
                [
                    pair_data,
                    convergence_data,
                    divergence_data,
                    assignment_data
                ]
            )

            if rank > max_rank:
                max_rank = rank
                max_assignment = predicted_assignment

        for i, note, voices in enumerate(zip(chord, max_assignment)):
            if assignment[i]:
                continue

            assignment[i] = (note, voices)
