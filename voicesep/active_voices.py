class ActiveVoices:

    def __init__(self):

        self.voices = []

    def insert(self, assignment):

        crossing = [False] * len(assignment)
        for i, right_voice in enumerate(assignment):
            for left_voice in right_voice.left:
                if self.crossing(left_voice.note, right_voice.note):
                    crossing[i] = True
                    break

        paired_voices = [
            voice for i, voice in enumerate(assignment)
            if voice.left and not crossing[i]
        ]
        unpaired_voices = [
            voice for i, voice in enumerate(assignment)
            if not voice.left or crossing[i]
        ]

        for right_voice in paired_voices:

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

            if left_voice.note is note:
                continue

            if left_voice.note.onset < note.onset:
                continue

            left_note = left_voice.note
            if note.pitch == left_note.pitch:
                return True

            for right_voice in left_voice.right:
                right_note = right_voice.note

                min_pitch = min(left_note.pitch, right_note.pitch)
                max_pitch = max(left_note.pitch, right_note.pitch)
                if min_pitch < note.pitch < max_pitch:
                    return True

        return False

    def crossing(self, left_note, right_note):

        right_note = voice.note

        for left_voice in voice.left:
            left_note = left_voice.note

            visited = set()
            for crossing_voice in self.voices:
                if crossing_voice.note.onset < left_note.onset or crossing_voice.note.onset > right_note.onset:
                    continue

                if crossing_voice in visited:
                    continue

                left_crossing_voices = []
                stack = [crossing_voice]
                while stack:
                    left_crossing_voice = stack.pop()
                    visited.add(left_crossing_voice)

                    appended = False
                    for left_left_crossing_voice in left_crossing_voice.left:
                        if left_left_crossing_voice.note.onset < left_note.onset:
                            continue

                        stack.append(left_left_crossing_voice)
                        appended = True

                    if not appended:
                        left_crossing_voices.append(left_crossing_voice)


                right_crossing_voices = []
                stack = [crossing_voice]
                while stack:
                    right_crossing_voice = stack.pop()
                    visited.add(right_crossing_voice)

                    appended = False
                    for right_right_crossing_voice in right_crossing_voice.left:
                        if right_right_crossing_voice.note.onset > right_note.onset:
                            continue

                        stack.append(right_right_crossing_voice)
                        appended = True

                    if not appended:
                        right_crossing_voices.append(right_crossing_voice)

                for left_crossing_voice, right_crossing_voice in itertools.product(left_crossing_voices, right_crossing_voices):
                    left_crossing_note = left_crossing_voice.note
                    right_crossing_note = right_crossing_voice.note

                    if not (
                        left_crossing_note.onset >= left_note.onset and
                        left_crossing_note.onset < right_note.onset and
                        right_crossing_note.onset > left_note.onset and
                        right_crossing_note.onset <= right_note.onset
                    ):
                        continue

                    if not (
                    ):
                        continue

                    crossed[i] = True
                    break

                else:
                    continue

                break

            else:
                continue

            break
