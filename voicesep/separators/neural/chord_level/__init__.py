import logging
import multiprocessing as mp

from voicesep.separators.neural.note_level import features


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

        max_combination = None
        max_rank = 0
        combination_generator = combinations.generate(
            chord,
            active_voices,
            assignment,
            self.convergence_limit,
            self.divergence_limit,
            part
        )
        for combination in combination_generator:

            data = features.generate(chord, combination, active_voices)
            rank = network.predict(data)

            if rank > max_rank:
                max_rank = rank
                max_combination = combination

        for i, note, voices in enumerate(zip(chord, max_combination)):
            if assignment[i]:
                continue

            right_voice = Voice(note)

            for left_voice in voices:
                left_voice.link(right_voice)

            assignment[i] = right_voice
