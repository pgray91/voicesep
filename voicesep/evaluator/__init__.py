import csv
import time

from voicesep.evaluator import pair_filters
from voicesep.evaluator.result import Result

class Evaluator:

    def __init__(self):

        self.results = {}

    def update(self, score, true_assignments, predicted_assignments, pair_filter):

        true_count = 0
        predicted_count = 0
        intersect_count = 0

        assignments = zip(true_assignments, predicted_assignments)
        for true_assignment, predicted_assignment in assignments:
            true_pairs, predicted_pairs = getattr(pair_filter, pair_filters)(
                true_assignment, predicted_assignment
            )

            true_count += len(true_pairs)
            predicted_count += len(predicted_pairs)
            intersect_count += len(set(true_pairs) & set(predicted_pairs))

        result = Result(score, true_count, predicted_count, intersect_count)

        self.results[pair_filter].append(result)

    def write(self, path):

        stamp = int(time.time())
        for pair_filter in self.results:
            with open("{}/{}.{}.csv".format(path, pair_filter, stamp), "w") as fp:
                csv_writer = csv.writer(fp)

                csv_writer.writerow(
                    [
                        "score",
                        "jaccard index",
                        "precision",
                        "recall",
                        "f1",
                        "true count",
                        "predicted count",
                        "intersect count",
                    ]
                )
                
                true_count = sum(
                    result.true_count() for result in self.results[pair_filter]
                )
                predicted_count = sum(
                    result.predicted_count() for result in self.results[pair_filter]
                )
                intersect_count = sum(
                    result.intersect_count() for result in self.results[pair_filter]
                )

                total = Result("[TOTAL]", true_count, predicted_count, intersect_count)

                for result in self.results[pair_filter] + [total]:
                    csv_writer.writerow(
                        [
                            result.name(),
                            result.jaccard_index(),
                            result.precision(),
                            result.recall(),
                            result.f1(),
                            result.true_count(),
                            result.predicted_count(),
                            result.intersect_count()
                        ]
                    )
