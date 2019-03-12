class ActiveVoices:

    def __init__(self, beat_horizon=None):

        self.voices = []
        self.inactive = set()
        self.watch = set()

        self.beat_horizon = beat_horizon

    def insert(self, assignment):

        unpaired_voices = []
        for right_voice in assignment:
            
            if not right_voice.left:
                unpaired_voices.append(right_voice)
                continue

            if any(
                self.crossing(left_voice.note, right_voice.note)
                for left_voice in right_voice.left
            ):
                unpaired_voices.append(right_voice)
                continue

            for left_voice in right_voice.left:
                if left_voice.note.pitch <= right_voice.note.pitch:
                    break

            i = (
                self.voices.index(left_voice) +
                (left_voice.note.pitch > right_voice.note.pitch)
            )
            while True:
                if i == len(self.voices):
                    break

                if self.voices[i].note.onset != right_voice.note.onset:
                    break

                i += 1

            self.voices.insert(i, right_voice)

        for right_voice in unpaired_voices:
            right_note = right_voice.note

            i = 0
            while i != len(self.voices):
                left_note = self.voices[i].note

                if left_note.pitch > right_note.pitch:
                    i += 1
                    continue

                for j, left_voice in enumerate(self.voices[i:], start=i+1):
                    left_note = left_voice.note

                    if not self.blocked(left_note):
                        break

                if left_note.pitch <= right_note.pitch:
                    break

                i = j

            self.voices.insert(i, right_voice)

        for voice in list(self.watch):
            if voice in self.voices:
                self.watch.remove(voice)
                self.inactive.add(voice)

    def filter(self, onset):

        if not self.beat_horizon:
            return

        self.voices = [
            voice for voice in self.voices
            if voice.note.onset >= onset - self.beat_horizon
        ]

        self.inactive = {
            voice for voice in self.inactive
            if voice.note.onset >= onset - self.beat_horizon
        }

    def deactivate(self, voice):

        if voice not in self.voices:
            self.watch.add(voice)
            return

        self.inactive.add(voice)

    def blocked(self, note):

        for left_voice in self.voices:

            left_note = left_voice.note

            if left_note is note:
                continue

            if left_note.onset < note.onset:
                continue

            if left_note.pitch == note.pitch:
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

            if any(
                left_voice.note.onset >= left_note_a.onset and
                left_voice.note != left_note_a
                for left_voice in left_voice_b.left
            ):
                continue

            if left_note_b.onset >= right_note_a.onset:
                continue

            stack = [left_voice_b]
            while stack:
                right_voice_b = stack.pop()
                right_note_b = right_voice_b.note

                if right_note_b is right_note_a:
                    continue

                if right_note_b.onset > right_note_a.onset:
                    continue

                if any(
                    right_voice.note.onset <= right_note_a.onset and
                    right_voice.note != right_note_a
                    for right_voice in right_voice_b.right
                ):
                    stack.extend(right_voice_b.right)
                    continue

                if right_note_b.onset <= left_note_a.onset:
                    continue

                if (
                    left_note_a.pitch <= left_note_b.pitch and
                    right_note_a.pitch >= right_note_b.pitch or
                    left_note_a.pitch >= left_note_b.pitch and
                    right_note_a.pitch <= right_note_b.pitch
                ):
                    return True

        return False

    def index(self, voice):

        return list(self).index(voice)

    def __len__(self):

        return len(self.voices) - len(self.inactive)

    def __getitem__(self, index):

        return tuple(iter(self))[index]

    def __iter__(self):

        return iter(
            voice for voice in self.voices if voice not in self.inactive
        )
