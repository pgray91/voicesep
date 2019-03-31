import inspect

from voicesep.separators.neural.network.features.feature import Feature


def find(module):

    return (
        feature for _, feature in inspect.getmembers(module, predicate=inspect.isclass)
        if Feature in inspect.getmro(feature) and feature != Feature
    )


def generate(module, *args, **kwargs):

    data = []
    for feature in find(module):
        data.extend(feature.generate(*args, **kwargs))

    return data


def count(module):

    return sum(len(feature.range()) for feature in find(module))
