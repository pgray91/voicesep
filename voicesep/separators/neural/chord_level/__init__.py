import logging


class ChordLevel(Separator):

    def __init__(
        self,
        score,
        network,
        convergence_limit=None,
        divergence_limit=None
    ):

        super().__init__(score)

        self.network = Network().open(network)
        self.convergence_limit = convergence_limit
        self.divergence_limit = divergence_limit

    def run(self, chord, active_voices, assignment):

        max_assignment = None
        max_rank = 0

        features = Features(chord, active_voices)

        assignment_generator = assignments.generate(
            chord,
            active_voices,
            assignment,
            self.convergence_limit,
            self.divergence_limit,
        )
        for predicted_assignment in assignment_generator:

            data = features.generate(predicted_assignment)
            rank = network.predict(data)

            if rank > max_rank:
                max_rank = rank
                max_assignment = predicted_assignment

        for i, note, voices in enumerate(zip(chord, max_assignment)):
            if assignment[i]:
                continue

            assignment[i] = (note, voices)
