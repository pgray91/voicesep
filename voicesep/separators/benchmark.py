import logging

from voicesep.separators.separator import Separator
from voicesep import Voice

logger = logging.getLogger(__name__)


class Benchmark(Separator):

    def __init__(self, score, one_to_many):

        super().__init__(score)

        self.one_to_many = one_to_many
        self.voice_map = {}
        self.voiceid_map = {}

        logger.debug("{} | initialization".format(__name__))

    def run(self, chord, active_voices, assignment):

        logger.info("{} | separating".format(chord))

        for i, note in enumerate(chord):
            right_voice = Voice(note)

            if self.one_to_many:
                if len(note.lyric) > 0:
                    voiceids = note.lyric
                    self.voiceid_map[note.color] = voiceids

                else:
                    voiceids = self.voiceid_map[note.color]

            else:
                voiceids = [note.color]

            for voiceid in voiceids:
                if voiceid in self.voice_map:
                    left_voice = self.voice_map[voiceid]
                    if right_voice not in left_voice.right:
                        left_voice.link(right_voice)

                self.voice_map[voiceid] = right_voice

            assignment[i] = right_voice
