import logging

logger = logging.getLogger(__name__)


def run(self, chord, active_voices, assignment, score, repeat_count):

    logger.info("{} separation".format(__name__))

    for i, note in enumerate(chord):
        if assignment[i]:
            continue

        left_notes = []
        left_index = max(0, chord.index - repeat_count)
        for left_chord in reversed(score[left_index:chord.index]):
            for left_note in left_chord:
                if left_note.pitch == note.pitch:
                    left_notes.append(left_note)
                    break

            else:
                break

        if len(left_notes) == 0:
            continue

        right_notes = []
        right_index = chord.index + repeat_count
        for right_chord in score[chord.index:right_index]:
            for right_note in right_chord:
                if right_note.pitch == note.pitch:
                    right_notes.append(right_note)
                    break

            else:
                break

        if len(left_notes) + len(right_notes) < repeat_count:
            continue

        left_note = left_notes[0]
        left_voice = active_voices[index of left_note]       

        right_voice = Voice(note)
        left_voice.append(right_voice)

        active_voices.deactivate(left_voice)

        assignment[i] = right_voice
