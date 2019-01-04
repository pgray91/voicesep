import abc


class Separator(abc.ABC):

    def __init__(self, score):

        self.score = score

    @abc.abstractmethod
    def run(self, chord, active_voices, assignment):

        pass
