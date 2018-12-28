class ActiveVoices:

    def __init__(self):

        self.voices = []

    def insert(self, voices):

        voices.sort(key=lambda voice: voice.note.pitch, reverse=True)
        
        crossed = [False] * len(voices)
        for i, voice in enumerate(voices):
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

        paired_voices = [
            voice for i, voice in enumerate(voices) if voice.left and not crossed[i]
        ]
        unpaired_voices = [
            voice for i, voice in enumerate(voices) if not voice.left or crossed[i]
        ]

        for voice in paired_voices:
            for i, left_voice in enumerate(self.voices):
                if voice in left_voice.right:
                    break

            if left_voice.note.pitch <= voice.note.pitch:
                self.voices.insert(i, voice)

            else:
                self.voices.insert(i + 1, voice)

        blocked = [False] * len(self.voices)
        for i, voice in enumerate(self.voices):
            note = voice.note

            for blocking_voice in self.voices:
                if voice is blocking_voice:
                    continue

                right_note = blocking_voice.note
                for left_voice in blocking_voice.left:
                    left_note = left_voice.note

                    if note.onset <= left_note.onset:
                        if (
                            note.pitch < left_note.pitch and
                            note.pitch < right_note.pitch or
                            note.pitch > left_note.pitch and
                            note.pitch < right_note.pitch
                        ):
                            blocked[i] = True
                            break

                else:
                    if note.onset < right_note.onset and note.pitch == right_note.pitch:
                        blocked[i] = True
                        break

                    continue

                break

        for voice in unpaired_voices:
            for i, left_voice in enumerate(self.voices):

                if blocked[i]:
                    continue

                if left_voice.note.pitch <= voice.note.pitch:
                    break

            self.voices.insert(i, voice)
