class Result:

    def __init__(self, name, benchmark_count, actual_count, intersect_count):

        self.name = name
        self.benchmark_count = benchmark_count
        self.actual_count = actual_count
        self.intersect_count = instersect_count

    def name(self):

        return self.name

    def benchmark_count(self):

        return self.benchmark_count

    def actual_count(self):

        return self.actual_count

    def intersect_count(self):

        return self.intersect_count

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
