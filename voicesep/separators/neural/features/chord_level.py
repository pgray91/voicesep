def create(chord):

    return [
        # Positional
        *[len(chord) == i for i in range(8)]
    ]
