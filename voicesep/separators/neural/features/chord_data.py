import voicesep.utils.constants as const
# INCLUDE CONST INTERVAL 
# DISCRETE

def create(chord):
  return [
    # Positional
    *[len(chord) == i for i in range(8)]
  ]
