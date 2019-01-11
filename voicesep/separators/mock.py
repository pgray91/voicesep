import logging

from voicesep.separators.separator import Separator

logger = logging.getLogger(__name__)


class Mock(Separator):

    def __init__(self, score, assignments):

        super.__init__(score)

        self.assignments = assignments

        logger.debug("{} | initializing".format(__name__))

    def run(self, chord, active_voices, assignment):

        for i in range(len(assignment)):
            assignment[i] = self.assignments[chord.index][i]
