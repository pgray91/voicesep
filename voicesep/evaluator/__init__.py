import csv
import logging
import time

from voicesep.evaluator import pair_filters
from voicesep.evaluator.result import Result

logger = logging.getLogger(__name__)


class Evaluator:

    def __init__(self):

        self.results = {}

        logger.debug("{} | initializing")

    def update(self, name, benchmark_assignments, actual_assignments, pair_filter):

        benchmark_count = 0
        actual_count = 0
        intersect_count = 0

        assignments = zip(benchmark_assignments, actual_assignments)
        for benchmark_assignment, actual_assignment in assignments:
            benchmark_pairs, actual_pairs = getattr(pair_filter, pair_filters)(
                benchmark_assignment, actual_assignment
            )

            benchmark_count += len(benchmark_pairs)
            actual_count += len(actual_pairs)
            intersect_count += len(set(benchmark_pairs) & set(actual_pairs))

        result = Result(name, benchmark_count, actual_count, intersect_count)

        self.results.getitem(pair_filter, []).append(result)

    def write(self, path):

        stamp = int(time.time())
        with open("{}/results.{}.csv".format(path, stamp), "w") as fp:
            csv_writer = csv.writer(fp)

            csv_writer.writerow(
                [
                    "score",
                    "jaccard index",
                    "precision",
                    "recall",
                    "f1",
                    "benchmark count",
                    "actual count",
                    "intersect count",
                    "pair filter"
                ]
            )

            for pair_filter in self.results:

                benchmark_count = sum(
                    result.benchmark_count() for result in self.results[pair_filter]
                )
                actual_count = sum(
                    result.actual_count() for result in self.results[pair_filter]
                )
                intersect_count = sum(
                    result.intersect_count() for result in self.results[pair_filter]
                )

                total = Result(
                    "[TOTAL]",
                    benchmark_count,
                    actual_count,
                    intersect_count
                )

                for result in self.results[pair_filter] + [total]:
                    csv_writer.writerow(
                        [
                            result.name(),
                            result.jaccard_index(),
                            result.precision(),
                            result.recall(),
                            result.f1(),
                            result.benchmark_count(),
                            result.actual_count(),
                            result.intersect_count(),
                            pair_filter
                        ]
                    )
