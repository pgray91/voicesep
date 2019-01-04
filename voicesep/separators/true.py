import logging

logger = logging.getLogger(__name__)


class True(Separator):

    def __init__(self, score, one_to_many):

        super(score)

        self.one_to_many = one_to_many
        self.voice_map = {}
        self.voiceid_map = {}

    def run(self, chord, active_voices, assignment):

        logger.info("{} separation".format(__name__))

        for i, note in enumerate(chord):
            right_voice = Voice(note)

            if one_to_many:
                if len(note.lyric) > 0:
                    voiceids = note.lyric
                    voiceid_map[note.color] = voiceids

                else:
                    voiceids = voiceid_map[note.color]

            else:
                voiceids = [note.color]

            for voiceid in voiceids:
                if voiceid in voice_map:
                    left_voice = voice_map[voiceid]
                    if right_voice not in left_voice.right:
                        left_voice.link(right_voice)

                voice_map[voiceid] = right_voice

            assignment[i] = right_voice
