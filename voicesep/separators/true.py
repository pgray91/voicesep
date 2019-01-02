import logging

logger = logging.getLogger(__name__)


def run(self, chord, active_voices, assignment, one_to_many, voice_map, voiceid_map):

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
