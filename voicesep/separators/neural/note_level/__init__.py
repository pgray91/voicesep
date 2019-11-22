import logging
import numpy as np

from voicesep.separators.neural.network import Network
from voicesep.separators.neural.network.features import Features
from voicesep.separators.neural.note_level.writer import Writer
from voicesep.separators.separator import Separator
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


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

        self.network = Network()
        self.network.read(network)

        self.assignment_threshold = assignment_threshold
        self.convergence_limit = convergence_limit
        self.divergence_limit = divergence_limit

        logger.debug(f"{__name__} | initialization")

    def run(self, chord, active_voices, assignment):

        logger.debug(f"{chord} | separating")

        features = Features(chord, active_voices)

        data = features.level(Features.Level.PAIR)

        note_count = len(chord)
        voice_count = len(active_voices) + 1

        ranks = self.network.predict([data]).reshape(note_count, voice_count)

        voice_mask = np.ones(ranks.shape)

        for i in range(note_count):

            if assignment[i] is None:
                continue

            voice_mask[i, :] = 0

        for i, voice in enumerate(active_voices if self.divergence_limit else []):

            if len(voice.right) < self.divergence_limit:
                continue

            voice_mask[:, i] = 0

        right_voices = [Voice(note) for note in chord]

        while note_count:
            max_index = np.argmax(np.multiply(ranks, voice_mask))
            note_index, voice_index = np.unravel_index(max_index, ranks.shape)

            if voice_mask[note_index][voice_index] == 0:
                note_count -= 1
                continue

            max_probability = ranks[note_index, voice_index]

            if (
                voice_index < voice_count - 1 and
                max_probability >= self.assignment_threshold
            ):
                right_voice = right_voices[note_index]
                left_voice = active_voices[voice_index]

                left_voice.link(right_voice)

                voice_mask[note_index, voice_index] = 0

                if len(right_voice.left) == self.convergence_limit:
                    voice_mask[note_index, :] = 0
                    note_count -= 1

                if len(left_voice.right) == self.divergence_limit:
                    voice_mask[:, voice_index] = 0

            else:
                voice_mask[note_index, :] = 0
                note_count -= 1

        for i in range(len(assignment)):
            if assignment[i]:
                continue

            assignment[i] = right_voices[i]


__all__ = [
    "NoteLevel",
    "Writer"
]
