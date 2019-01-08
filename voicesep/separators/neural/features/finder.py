import inspect


def find(module):

    return (
        feature for _, feature in inspect.getmembers(level)
        if Feature in inspect.getmro(feature)
    )

def generate(module, **kwargs):

    data = []
    for feature in find(module):
        data.extend(feature.generate(**kwargs))

    return data

def count(module):

    return sum(len(feature.range()) for feature in find(module))
