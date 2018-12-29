class ActiveVoices:

    def __init__(self):

        self.voices = []

    def insert(self, assignment):

        unpaired_voices = []
        for right_voice in assignment:
            
            if not right_voice.left:
                upaired_voices.append(right_voice)
                continue

            if any(
                self.crossing(left_voice.note, right_voice.note)
                for left_voice in right_voice.left
            ):
                upaired_voices.append(right_voice)
                continue

            for left_voice in right_voice.left:
                if left_voice.note.pitch <= right_voice.note.pitch:
                    break

            i = (
                self.voices.index(left_voice) +
                left_voice.note.pitch > right_voice.note.pitch
            )
            while True:
                if i == len(self.voices):
                    break

                if self.voices[i].note.onset != right_voice.note.onset:
                    break

                i += 1

            self.voices.insert(i, right_voice)

        for right_voice in unpaired_voices:

            j = -1
            for i, left_voice in enumerate(self.voices):

                if self.blocked(left_voice.note):
                    continue

                j = i
                if left_voice.note.pitch <= right_voice.note.pitch:
                    break

            else:
                j += 1

            self.voices.insert(j, right_voice)

    def filter(self, onset, beat_horizon):
        pass

    def blocked(self, note):

        for left_voice in self.voices:

            left_note = left_voice.note

            if left_note is note:
                continue

            if left_note.onset < note.onset:
                continue

            if note.pitch == left_note.pitch:
                return True

            for right_voice in left_voice.right:
                right_note = right_voice.note

                min_pitch = min(left_note.pitch, right_note.pitch)
                max_pitch = max(left_note.pitch, right_note.pitch)
                if min_pitch < note.pitch < max_pitch:
                    return True

        return False

    def crossing(self, left_note_a, right_note_a):

        for left_voice_b in self.voices:
            left_note_b = left_voice_b.note

            if left_note_b is left_note_a:
                continue

            if left_note_b.onset < left_note_a.onset:
                continue

            if left_note_b.onset >= right_note_a.onset:
                continue

            if any(
                left_voice.note.onset >= left_note_a.onset
                for left_voice in left_voice_b.left
            ):
                continue

            stack = [left_voice_b]
            while stack:
                voice_b = stack.pop()

                for right_voice_b in voice_b.right:
                    right_note_b = right_voice_b.note

                    if right_note_b.onset > right_note_a.onset:
                        continue

                    if any(
                        right_voice.note.onset <= right_note_a.onset
                        for right_voice in right_voice_b.right
                    ):
                        stack.append(right_voice_b)
                        continue

                    min_pitch_a = min(left_note_a.pitch, right_note_a.pitch)
                    max_pitch_a = max(left_note_a.pitch, right_note_a.pitch)

                    min_pitch_b = min(left_note_b.pitch, right_note_b.pitch)
                    max_pitch_b = max(left_note_b.pitch, right_note_b.pitch)

                    if (
                        min_pitch_a <= min_pitch_b < max_pitch_a and
                        min_pitch_a < max_pitch_b <= max_pitch_a
                    ):
                        return True

        return False
