class Assignments:

    def __init__(self):

        self.assignments = []

    def append(self, assignment):

        self.assignments.append(assignment)

    def pairs(self):

        pairs = set()
        for assignment in self.assignments:
            for voice in assignment:
                for right_voice in voice.right:
                    pair = (voice.note, right_voice.note)
                    pairs.add(pair)

        return pairs

    def __len__(self):

        return len(self.assignments)

    def __getitem__(self, index):

        return self.assignments[index]

    def __iter__(self):

        return iter(self.assignments)
