import datetime
import logging


def format(logger, debug=True, stdout=True):

    if debug:
        logger.setLevel(logging.DEBUG)

    handlers = []

    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    handlers.append(logging.FileHandler(f"/tmp/voicesep/{now}.log"))
    if stdout:
        handlers.append(logging.StreamHandler())

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(funcName)s - line %(lineno)d | "
        "%(message)s"
    )

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
