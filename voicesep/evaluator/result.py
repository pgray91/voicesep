import logging

logger = logging.getLogger(__name__)


class Result:

    def __init__(self, name, benchmark_count, actual_count, intersect_count):

        self.name = name
        self.benchmark_count = benchmark_count
        self.actual_count = actual_count
        self.intersect_count = instersect_count

        logger.debug("{} | initializing".format(name))

    def precision(self):

        numerator = self.intersect_count
        denominator = self.actual_count

        return -1 if denominator == 0 else numerator / denominator

    def recall(self):

        numerator = self.intersect_count
        denominator = self.benchmark_count

        return -1 if denominator == 0 else numerator / denominator

    def jaccard_index(self):

        numerator = self.intersect_count
        denominator = self.actual_count + self.benchmark_count - self.intersect_count

        return -1 if denominator == 0 else numerator / denominator

    def f1(self):

        numerator = 2 * self.intersect_count
        denominator = benchmark_count + actual_count

        return -1 if denominator == 0 else numerator / denominator
