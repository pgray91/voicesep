import numpy as np

from voicesep.separators.neural.note_level.features import Features

def separate(
    score,
    network,
    assignment_threshold,
    convergence_limit,
    divergence_limit,
    beat_horizon
):

    assignments = Assignments()
    active_voices = ActiveVoices()
    features = Features()

    for chord in score:
        active_voices.filter(chord.onset, beat_horizon)

        right_voices = [Voice(note) for note in chord]

        data = features.generate(chord, active_voices)
        voice_count = len(active_voices) + 1

        ranks = network.predict(data).reshape(len(chord), voice_count)
        voice_mask = np.ones((ranks.shape))

        voice_limits = [divergence_limit - len(voice.right) for voice in active_voices]
        note_count = len(chord)

        while note_count:
            max_index = np.argmax(np.multiply(ranks, voice_mask))
            note_index, voice_index = np.unravel_index(max_index, ranks.shape)

            max_probability = ranks[note_index, voice_index]
            assert max_probability != 0

            if voice_index < voice_count - 1 and max_probability >= assignment_threshold:
                left_voice = active_voices[voice_index]
                right_voice = right_voices[note_index]

                left_voice.append(right_voice)

                voice_mask[note_index, voice_index] = 0

                if len(right_voice.left) == convergence_limit:
                    voice_mask[note_index, :] = 0
                    note_count -= 1

                if len(left_voice.right) == divergence_limit:
                    voice_mask[:, voice_index] = 0

            else:
                voice_mask[note_index, :] = 0
                note_count -= 1

        assignments.append(right_voices)

        active_voices.insert(right_voices)
