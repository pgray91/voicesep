def separate(score):

    pairs = set()

    active_voices = ActiveVoices()
    for chord in score:

        left_voices = [
            voice for voice in active_voices
            if voice.beat_offset <= chord.beat_onset
        ]

        right_voices = [Voice(note) for note in chord]

        for left_voice, right_voice in zip(left_voices, right_voices):
            connect(left_voice, right_voice)

            pairs.insert((left_voice.note, right_voice.note))
            # Consider creating a pairs class that inherits from set

        for voice in right_voices:
            active_voices.insert(voice)

    return pairs
