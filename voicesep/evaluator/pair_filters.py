def pairs(assignment):

    pairs = set()
    for voice in assignment:
        for left_voice in voice.left:
            pair = (left_voice.note, voice.note)
            pairs.add(pair)

    return pairs

def all(benchmark_assignment, actual_assignment):

    return pairs(benchmark_assignment), pairs(actual_assignment)

def exclude_rests(benchmark_assignment, actual_assignment):

    benchmark_pairs = [
        pair for pair in pairs(benchmark_assignment)
        if pair[0].beat_offset >= pair[1].beat_onset
    ]

    actual_pairs = [
        pair for pair in pairs(actual_assignment)
        if pair[0].beat_offset >= pair[1].beat_onset
    ]

    return benchmark_pairs, actual_pairs

def joint_many(benchmark_assignment, actual_assignment):

    assignment = zip(benchmark_assignment, actual_assignment)
    for benchmark_voice, actual_voice in assignment:

        if len(benchmark_voice.left) > 1 or len(actual_voice.left) > 1:
            break

        if len(benchmark_voice.left) == 1 and len(next(benchmark_voice.left).right) > 1:
            break

        if len(actual_voice.left) == 1 and len(next(actual_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(benchmark_assignment), pairs(actual_assignment)

def benchmark_joint_many(benchmark_assignment, actual_assignment):

    for benchmark_voice in benchmark_assignment:

        if len(benchmark_voice.left) > 1:
            break

        if len(benchmark_voice.left) == 1 and len(next(benchmark_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(benchmark_assignment), pairs(actual_assignment)

def actual_joint_many(benchmark_assignment, actual_assignment):

    for actual_voice in actual_assignment:

        if len(actual_voice.left) > 1:
            break

        if len(actual_voice.left) == 1 and len(next(actual_voice.left).right) > 1:
            break

    else:
        return set(), set()

    return pairs(benchmark_assignment), pairs(actual_assignment)

def joint_one(benchmark_assignment, actual_assignment):

    for benchmark_voice in benchmark_assignment:

        if len(benchmark_voice.left) == 0:
            continue

        if len(benchmark_voice.left) == 1 and len(next(benchmark_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(benchmark_assignment), pairs(actual_assignment)

    for actual_voice in actual_assignment:

        if len(actual_voice.left) == 0:
            continue

        if len(actual_voice.left) == 1 and len(next(actual_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(benchmark_assignment), pairs(actual_assignment)

    return set(), set()


def benchmark_joint_one(benchmark_assignment, actual_assignment):

    for benchmark_voice in benchmark_assignment:

        if len(benchmark_voice.left) == 0:
            continue

        if len(benchmark_voice.left) == 1 and len(next(benchmark_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(benchmark_assignment), pairs(actual_assignment)

    return set(), set()


def actual_joint_one(benchmark_assignment, actual_assignment):

    for actual_voice in actual_assignment:

        if len(actual_voice.left) == 0:
            continue

        if len(actual_voice.left) == 1 and len(next(actual_voice).left.right) == 1:
            continue

        break

    else:
        return pairs(benchmark_assignment), pairs(actual_assignment)

    return set(), set()

def many(benchmark_assignment, actual_assignment):

    benchmark_many = []
    actual_many = []

    assignment = zip(benchmark_assignment, actual_assignment)
    for benchmark_voice, actual_voice in assignment:

        elif len(benchmark_voice.left) > 1 or len(actual_voice.left) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)

        elif len(benchmark_voice.left) == 1 and len(next(benchmark_pairs).left.right) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)

        elif len(actual_voice.left) == 1 and len(next(actual_voice).left.right) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)
   
    return pairs(benchmark_many), pairs(actual_many)

def benchmark_many(benchmark_assignment, actual_assignment):

    benchmark_many = []
    actual_many = []

    for benchmark_voice in benchmark_assignment:

        if len(benchmark_voice.left) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)

        elif len(benchmark_voice.left) == 1 and len(next(benchmark_pairs).left.right) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)
   
    return pairs(benchmark_many), pairs(actual_many)

def actual_many(benchmark_assignment, actual_assignment):

    benchmark_many = []
    actual_many = []

    for actual_voice in actual_assignment:

        if len(actual_voice.left) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)

        elif len(actual_voice.left) == 1 and len(next(actual_voice).left.right) > 1:
            benchmark_many.append(benchmark_voice)
            actual_many.append(actual_voice)
   
    return pairs(benchmark_many), pairs(actual_many)

def one(benchmark_assignment, actual_assignment):

    benchmark_one = []
    actual_one = []

    assignment = zip(benchmark_assignment, actual_assignment)
    for benchmark_voice, actual_voice in assignment:

        if len(benchmark_voice.left) == 0 or len(actual_voice.left) == 0:
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

        elif len(benchmark_voice.left) == 1 and len(next(benchmark_voice).left.right) == 1
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

        elif len(actual_voice.left) == 1 and len(next(actual_voice).left.right) == 1
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

    return pairs(benchmark_one), pairs(actual_one)

def benchmark_one(benchmark_assignment, actual_assignment):

    benchmark_one = []
    actual_one = []

    for benchmark_voice in benchmark_assignment:

        if len(benchmark_voice.left) == 0:
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

        elif len(benchmark_voice.left) == 1 and len(next(benchmark_voice).left.right) == 1
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

    return pairs(benchmark_one), pairs(actual_one)

def actual_one(benchmark_assignment, actual_assignment):

    benchmark_one = []
    actual_one = []

    for actual_voice in actual_assignment:

        if len(actual_voice.left) == 0:
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

        elif len(actual_voice.left) == 1 and len(next(actual_voice).left.right) == 1
            benchmark_one.append(benchmark_voice)
            actual_one.append(actual_voice)

    return pairs(benchmark_one), pairs(actual_one)
