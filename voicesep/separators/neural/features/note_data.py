import voicesep.utils.constants as const

def create(note):

    return [
        # Pitch
        *(
            lower <= note.pitch and
            note.pitch < upper
            for lower, upper in range(40, 80)
        )

        # Temporal
        *[
            lower <= note.duration and
            note.duration < upper
            for lower, upper in range(0, 5, 0.25)
        ]

        # Positional
        *[note.index == i for i in range(8)]
    ]
