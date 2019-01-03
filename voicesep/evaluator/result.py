class Result:

    def __init__(self, name, true_count, predicted_count, intersect_count):

        self.name = name
        self.true_count = true_count
        self.predicted_count = predicted_count
        self.intersect_count = instersect_count

    def name(self):

        return self.name

    def true_count(self):

        return self.true_count

    def predicted_count(self):

        return self.predicted_count

    def intersect_count(self):

        return self.intersect_count

    def precision(self):

        numerator = self.intersect_count
        denominator = self.predicted_count

        return -1 if denominator == 0 else numerator / denominator

    def recall(self):

        numerator = self.intersect_count
        denominator = self.true_count

        return -1 if denominator == 0 else numerator / denominator

    def jaccard_index(self):

        numerator = self.intersect_count
        denominator = self.predicted_count + self.true_count - self.intersect_count

        return -1 if denominator == 0 else numerator / denominator

    def f1(self):

        numerator = 2 * self.intersect_count
        denominator = true_count + predicted_count

        return -1 if denominator == 0 else numerator / denominator
