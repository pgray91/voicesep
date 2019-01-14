import numpy as np

from voicesep.separators.neural.note_level import features


class NoteLevel(Separator):

    def __init__(
        self,
        score,
        network,
        assignment_threshold,
        convergence_limit=None,
        divergence_limit=None
    ):

        super().__init__(score)

        self.network = Network().open(network)
        self.assignment_threshold = assignment_threshold
        self.convergence_limit = convergence_limit
        self.divergence_limit = divergence_limit

    def run(self, chord, active_voices, assignment):

        right_voices = [Voice(note) for note in chord]

        data = []
        for note in chord:
            for voice in active_voice:
                data.append(features.generate(note, chord, voice))

            data.append(features.generate(note, chord, None))

        note_count = len(chord)
        voice_count = len(active_voices) + 1

        ranks = network.predict(data).reshape(note_count, voice_count)

        voice_mask = np.ones(ranks.shape)

        for i in range(note_count):
            voice_mask[i, :] = assignment[i] is not None

        for i, voice in enumerate(active_voices):
            voice_mask[:, i] = (
                divergence_limit is None or
                len(voice.right) < divergence_limit
            )

        while note_count:
            max_index = np.argmax(np.multiply(ranks, voice_mask))
            note_index, voice_index = np.unravel_index(max_index, ranks.shape)

            max_probability = ranks[note_index, voice_index]

            if voice_index < voice_count - 1 and max_probability >= assignment_threshold:
                right_voice = right_voices[note_index]
                left_voice = active_voices[voice_index]

                left_voice.link(right_voice)

                voice_mask[note_index, voice_index] = 0

                if len(right_voice.left) == convergence_limit:
                    voice_mask[note_index, :] = 0
                    note_count -= 1

                if len(left_voice.right) == divergence_limit:
                    voice_mask[:, voice_index] = 0

            else:
                voice_mask[note_index, :] = 0
                note_count -= 1

        for i in range(len(assignment)):
            if assignment[i]:
                continue

            assignment[i] = right_voices[i]
