import abc


class Feature(abc.ABC):

    @abc.abstractmethod
    def generate(*args, **kwargs):

        pass

    def range():

        return range(1)
