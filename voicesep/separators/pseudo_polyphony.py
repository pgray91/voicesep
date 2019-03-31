import logging

from voicesep.separators.separator import Separator
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


class PseudoPolyphony(Separator):

    def __init__(self, score, repeat_limit):

        super().__init__(score)

        self.repeat_limit = repeat_limit

        logger.debug("{} | initialization".format(__name__))

    def run(self, chord, active_voices, assignment):

        logger.info("{} separation".format(__name__))

        for i, note in enumerate(chord):
            if assignment[i]:
                continue

            duration = note.duration

            if (
                active_voices.beat_horizon and
                note.duration * 2 > active_voices.beat_horizon
            ):
                continue

            left_notes = []
            left_index = chord.index - 1
            repeat_count = 0
            while left_index >= 0 and repeat_count < self.repeat_limit:

                left_chord = self.score[left_index]
                left_index -= 1

                right_note = left_notes[-1] if left_notes else note
                left_offset = left_chord.onset + duration * 2

                if left_offset > right_note.onset:
                    if any(
                        left_note.pitch == right_note.pitch
                        for left_note in left_chord
                    ):
                        break

                    continue

                if left_offset < right_note.onset:
                    break

                for left_note in left_chord:
                    if (
                        left_note.pitch == right_note.pitch and
                        left_note.duration == right_note.duration
                    ):
                        left_notes.append(left_note)
                        break

                else:
                    break

                repeat_count += 1

            right_notes = []
            right_index = chord.index + 1
            repeat_count = 0
            while right_index < len(self.score) and repeat_count < self.repeat_limit:

                right_chord = self.score[right_index]
                right_index += 1

                left_note = right_notes[-1] if right_notes else note
                right_offset = right_chord.onset - duration * 2

                if right_offset < left_note.onset:
                    if any(
                        right_note.pitch == left_note.pitch
                        for right_note in right_chord
                    ):
                        break

                    continue

                if right_offset > left_note.onset:
                    break

                for right_note in right_chord:
                    if (
                        right_note.pitch == left_note.pitch and
                        right_note.duration == left_note.duration
                    ):
                        right_notes.append(right_note)
                        break

                else:
                    break

                repeat_count += 1

            if len(left_notes) + len(right_notes) < self.repeat_limit:
                continue

            right_voice = Voice(note)
            if left_notes:
                left_note = left_notes[0]
                left_voice = next(
                    voice for voice in active_voices.inactive if voice.note == left_note
                )

                left_voice.link(right_voice)

            active_voices.deactivate(right_voice)
            assignment[i] = right_voice
