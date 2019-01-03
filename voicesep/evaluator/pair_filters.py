def pairs(assignment):

    pairs = set()
    for voice in assignment:
        for left_voice in voice.left:
            pair = (left_voice.note, voice.note)
            pairs.add(pair)

    return pairs

def all(true_assignment, predicted_assignment):

    return pairs(true_assignment), pairs(predicted_assignment)

def exclude_rests(true_assignment, predicted_assignment):

    true_pairs = [
        pair for pair in pairs(true_assignment)
        if pair[0].beat_offset >= pair[1].beat_onset
    ]

    predicted_pairs = [
        pair for pair in pairs(predicted_assignment)
        if pair[0].beat_offset >= pair[1].beat_onset
    ]

    return true_pairs, predicted_pairs

def joint_many(true_assignment, predicted_assignment):

    for true_voice, predicted_voice in zip(true_assignment, predicted_assignment):

        if len(true_voice.left) > 1 or len(predicted_voice.left) > 1:
            break

        if len(true_voice.left) == 1 and len(next(true_voice.left).right) > 1:
            break

        if len(predicted_voice.left) == 1 and len(next(predicted_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(true_assignment), pairs(predicted_assignment)

def true_joint_many(true_assignment, predicted_assignment):

    for true_voice in true_assignment:

        if len(true_voice.left) > 1:
            break

        if len(true_voice.left) == 1 and len(next(true_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(true_assignment), pairs(predicted_assignment)

def predicted_joint_many(true_assignment, predicted_assignment):

    for predicted_voice in predicted_assignment:

        if len(predicted_voice.left) > 1:
            break

        if len(predicted_voice.left) == 1 and len(next(predicted_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(true_assignment), pairs(predicted_assignment)

def joint_one(true_assignment, predicted_assignment):

    for true_voice in true_assignment:

        if len(true_voice.left) == 0:
            continue

        if len(true_voice.left) == 1 and len(next(true_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(true_assignment), pairs(predicted_assignment)

    for predicted_voice in predicted_assignment:

        if len(predicted_voice.left) == 0:
            continue

        if len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(true_assignment), pairs(predicted_assignment)

    return set(), set()


def true_joint_one(true_assignment, predicted_assignment):

    for true_voice in true_assignment:

        if len(true_voice.left) == 0:
            continue

        if len(true_voice.left) == 1 and len(next(true_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(true_assignment), pairs(predicted_assignment)

    return set(), set()


def predicted_joint_one(true_assignment, predicted_assignment):

    for predicted_voice in predicted_assignment:

        if len(predicted_voice.left) == 0:
            continue

        if len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(true_assignment), pairs(predicted_assignment)

    return set(), set()

def many(true_assignment, predicted_assignment):

    true_many = []
    predicted_many = []

    for true_voice, predicted_voice in zip(true_assignment, predicted_assignment):

        elif len(true_voice.left) > 1 or len(predicted_voice.left) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)

        elif len(true_voice.left) == 1 and len(next(true_pairs).left.right) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)

        elif len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)
   
    return pairs(true_many), pairs(predicted_many)

def true_many(true_assignment, predicted_assignment):

    true_many = []
    predicted_many = []

    for true_voice in true_assignment:

        if len(true_voice.left) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)

        elif len(true_voice.left) == 1 and len(next(true_pairs).left.right) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)
   
    return pairs(true_many), pairs(predicted_many)

def predicted_many(true_assignment, predicted_assignment):

    true_many = []
    predicted_many = []

    for predicted_voice in predicted_assignment:

        if len(predicted_voice.left) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)

        elif len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) > 1:
            true_many.append(true_voice)
            predicted_many.append(predicted_voice)
   
    return pairs(true_many), pairs(predicted_many)

def one(true_assignment, predicted_assignment):

    true_one = []
    predicted_one = []

    for true_voice, predicted_voice in zip(true_assignment, predicted_assignment):

        if len(true_voice.left) == 0 or len(predicted_voice.left) == 0:
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

        elif len(true_voice.left) == 1 and len(next(true_voice).left.right) == 1
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

        elif len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) == 1
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

    return pairs(true_one), pairs(predicted_one)

def true_one(true_assignment, predicted_assignment):

    true_one = []
    predicted_one = []

    for true_voice in true_assignment:

        if len(true_voice.left) == 0:
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

        elif len(true_voice.left) == 1 and len(next(true_voice).left.right) == 1
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

    return pairs(true_one), pairs(predicted_one)

def predicted_one(true_assignment, predicted_assignment):

    true_one = []
    predicted_one = []

    for predicted_voice in predicted_assignment:

        if len(predicted_voice.left) == 0:
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

        elif len(predicted_voice.left) == 1 and len(next(predicted_voice).left.right) == 1
            true_one.append(true_voice)
            predicted_one.append(predicted_voice)

    return pairs(true_one), pairs(predicted_one)
