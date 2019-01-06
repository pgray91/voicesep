import argparse
import logging
import music21 as m21

logger = logging.getLogger(__name__)


def validate_annotations(sheet, beat_horizon):

    score = m21.converter.parse(sheet)

    chords = score.flat.notes.stream()
    chord_groups = chords.groupElementsByOffset()
    for chord_group in chord_groups:
        note_index = 0
        for chord_part in chord_group:
            if chord_part.duration.isGrace:
                continue


            note_group = chord_part if chord_part.isChord else [chord_part]
            for note_part in sorted(note_group, reverse=True):
                continue

            logger.warn("")

def validate_scale(sheet):

    score = m21.converter.parse(sheet)

    measures = score.semiFlat.getElementsByClass("Measure").stream()
    measure_groups = map(
        m21.stream.Stream,
        m21.stream.iterator.OffsetIterator(measures)
    )
    for measure_index, measure_group in enumerate(measure_groups, start=1):
        top_measure = measure_group[0]

        if top_measure.getElementsByClass("KeySignature"):
            logger.debug("m{} | changing key signature".format(measure_index))

            keysig = top_measure.getElementsByClass("KeySignature")[0]
            scale = keysig.getScale()

        chords = measure_group.flat.notes.stream()
        chord_groups = m21.stream.iterator.OffsetIterator(chords)
        for chord_index, chord_group in enumerate(chord_groups, start=1):
            note_index = 0
            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue


                note_group = chord_part if chord_part.isChord else [chord_part]
                for note_part in sorted(note_group, reverse=True):
                    continue

                logger.warn("")

                degree = scale.getScaleDegreeFromPitch(
                    note_part.name, comparisonAttribute="step"
                )

def main():
    pass


if __name__ == "__main__":
    main()
