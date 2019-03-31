import argparse
import logging
import music21 as m21

from fractions import Fraction as F

import voicesep as vs

logger = logging.getLogger()
logger.level(logging.INFO)


def validate_time_signature(args):
    pass

def validate_annotations(args):

    sheet = args.sheet
    beat_horizon = args.beat_horizon

    score = m21.converter.parse(sheet)

    color_map = {}
    id_map = {}
    pair_map = {}

    denomination = 0

    onset_origin = F()
    ql_origin = F()

    measures = score.semiFlat.getElementsByClass("Measure").stream()
    measure_groups = map(
        m21.stream.Stream,
        m21.stream.iterator.OffsetIterator(measures)
    )
    for measure_index, measure_group in enumerate(measure_groups, start=1):
        top_measure = measure_group[0]

        if top_measure.getElementsByClass("TimeSignature"):
            logger.debug("m{} | changing time signature".format(measure_index))

            ql_distance = top_measure.offset - ql_origin

            onset_origin += ql_distance * denomination / vs.Score.QUARTER
            ql_origin = F(top_measure.offset)

            timesig = top_measure.getElementsByClass("TimeSignature")[0]
            denomination = timesig.denominator

        chords = measure_group.flat.notes.stream()
        chord_groups = m21.stream.iterator.OffsetIterator(chords)
        for chord_index, chord_group in enumerate(chord_groups, start=1):
            top_chord = chord_group[0]

            ql_distance = top_chord.offset - ql_origin
            onset = onset_origin + ql_distance * denomination / vs.Score.QUARTER

            onset_colors = {}
            onset_ids = {}
            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue

                lyrics = [lyric.text.split(",") for lyric in chord_part.lyrics]

                note_group = chord_part if chord_part.isChord else [chord_part]
                for part_index, note_part in enumerate(reversed(note_group)):

                    note = vs.Note(
                        name=note_part.name,
                        octave=note_part.octave,
                        location=(measure_index, chord_index),
                        onset=onset
                    )

                    assert part_index < len(lyrics) if lyrics else True, "{} | {}".format(
                        note, "missing lyric"
                    )

                    lyric = lyrics[part_index] if lyrics else []
                    color = note_part.style.color

                    assert color != "#000000" and color is not None, "{} | {}".format(
                        note, "black"
                    )

                    assert not any(id_ in onset_ids for id_ in lyric), "{} | {}".format(
                        note, "duplicate id"
                    )

                    assert color not in onset_colors, "{} | {}".format(
                        note, "duplicate color"
                    )

                    assert color in color_map or lyric, "{} | {}".format(
                        note, "missing lyric"
                    )

                    assert (
                        color_map[color][0] == lyric[0] if color in color_map and lyric
                        else True
                    ), (
                        "{} | {}".format(
                            note,
                            "leading id changed from {} to {}".format(
                                color_map[color][0], lyric[0]
                            )
                        )
                    )

                    if lyric:
                        color_map[color] = lyric

                    if color_map[color][0] in id_map:

                        assert id_map[color_map[color][0]] == color, "{} | {}".format(
                            note, "color changed from leading id {} to {}".format(
                                id_map[color_map[color][0]], color
                            )
                        )

                    id_map[color_map[color][0]] = color

                    for id_ in color_map[color]:

                        if id_ in pair_map:
                            left_note = pair_map[id_]

                            if note.onset - left_note.onset > beat_horizon:
                                logger.warning(
                                    "{} - {} | {}".format(
                                        left_note, note, "beat horizon exceeded"
                                    )
                                )
                        
                        pair_map[id_] = note

    for id_, note in pair_map.items():
        logger.info("{} | last use of id {}".format(note, id_))

# def validate_scale(sheet):
#
#     score = m21.converter.parse(sheet)
#
#     measures = score.semiFlat.getElementsByClass("Measure").stream()
#     measure_groups = map(
#         m21.stream.Stream,
#         m21.stream.iterator.OffsetIterator(measures)
#     )
#     for measure_index, measure_group in enumerate(measure_groups, start=1):
#         top_measure = measure_group[0]
#
#         if top_measure.getElementsByClass("KeySignature"):
#             logger.debug("m{} | changing key signature".format(measure_index))
#
#             keysig = top_measure.getElementsByClass("KeySignature")[0]
#             scale = keysig.getScale()
#
#         chords = measure_group.flat.notes.stream()
#         chord_groups = m21.stream.iterator.OffsetIterator(chords)
#         for chord_index, chord_group in enumerate(chord_groups, start=1):
#             note_index = 0
#             for chord_part in chord_group:
#                 if chord_part.duration.isGrace:
#                     continue
#
#
#                 note_group = chord_part if chord_part.isChord else [chord_part]
#                 for note_part in sorted(note_group, reverse=True):
#                     continue
#
#                 logger.warn("")
#
#                 degree = scale.getScaleDegreeFromPitch(
#                     note_part.name, comparisonAttribute="step"
#                 )

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--sheet", type=str, required=True)

    validators = parser.add_subparsers(dest="validator")
    validators.required = True

    annotations = validators.add_parser("annotations")
    annotations.add_argument("-b", "--beat_horizon", type=int, required=True)

    scale = validators.add_parser("scale")

    args = parser.parse_args()

    globals()["validate_{}".format(args.validator)](args)


if __name__ == "__main__":
    main()
