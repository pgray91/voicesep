import voicesep.utils.constants as const
# INCLUDE CONST INTERVAL 
# DISCRETE

def create(note, interval):

  return [
    # Pitch
    *(
      lower <= note.pitch_space and note.pitch_space < upper
      for lower, upper in range(40, 80)
    )

    # Temporal
    *[lower <= note.duration and note.duration < upper for lower, upper in range(0, 5, 0.25)]

    # Positional
    *[note.index == i for i in range(8)]
  ]
