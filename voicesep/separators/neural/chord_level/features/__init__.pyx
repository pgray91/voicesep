#cython: language_level=3
import cython
import numpy as np
import theano

from voicesep.separators.neural.chord_level.features.levels cimport (
  note_features, voice_features, pair_features,
  conv_features, div_features, assign_features
)
from voicesep.separators.neural.chord_level.features.assignments_generator \
  cimport (AssignmentsGenerator)

cdef class Features:
  GROUP_NAMES = ["pair", "conv", "div"]
  GROUP_COUNTS = [
    pair_features.COUNT + note_features.COUNT + voice_features.COUNT,
    conv_features.COUNT + note_features.COUNT, 
    div_features.COUNT + voice_features.COUNT
  ]
  GROUP_PADS = [pair_features.PAD, conv_features.PAD, div_features.PAD]

  # IND_COUNT = assign_features.COUNT + note_features.COUNT + voice_features.COUNT
  IND_COUNT = assign_features.COUNT

  cdef AssignmentsGenerator assignments_generator

  cdef float[:,::1] pair_data, conv_data, div_data, assign_data
  cdef float[:,::1] note_data, voice_data
  cdef float[:,::1] ind_data

  cdef float[:,::1] all_note_data, all_voice_data
  cdef float[:,:,::1] all_pair_data

  cdef int pair_index, conv_index, div_index, ind_index 

  cdef int call_num, assign_limit

  def __cinit__(
    self, size_t max_rows, size_t assign_limit, size_t random_limit,
    size_t conv_limit, size_t div_limit, size_t pp_limit,
    bint lookback, bint allow_cross, size_t batch_size
  ):
    self.assignments_generator = AssignmentsGenerator(
      max_rows, assign_limit, random_limit,
      conv_limit, div_limit, pp_limit,
      lookback, allow_cross
    )

    self.pair_data = np.empty(
      (
        max_rows * pair_features.PAD * batch_size, 
        pair_features.COUNT + note_features.COUNT + voice_features.COUNT
      ), theano.config.floatX
    )
    self.conv_data = np.empty(
      (
        max_rows * conv_features.PAD * batch_size, 
        conv_features.COUNT + note_features.COUNT
      ), theano.config.floatX
    )
    self.div_data = np.empty(
      (
        max_rows * div_features.PAD * batch_size, 
        div_features.COUNT + voice_features.COUNT
      ), theano.config.floatX
    )

    self.ind_data = np.empty(
      (
        max_rows * batch_size,
        assign_features.COUNT + note_features.COUNT + voice_features.COUNT
      ), theano.config.floatX
    )

    self.assign_data = self.ind_data[:, :assign_features.COUNT]
    self.note_data = self.ind_data[
      :, assign_features.COUNT : note_features.COUNT
    ]
    self.voice_data = self.ind_data[
      :, assign_features.COUNT + note_features.COUNT :
    ]

    self.all_note_data = np.empty(
      (10, note_features.COUNT),
      dtype=theano.config.floatX
    )
    self.all_voice_data = np.empty(
      (70, voice_features.COUNT),
      dtype=theano.config.floatX
    )
    self.all_pair_data = np.empty(
      (10, 70, pair_features.COUNT),
      dtype=theano.config.floatX
    )

    self.pair_index = 0
    self.conv_index = 0
    self.div_index = 0
    self.ind_index = 0

    self.call_num = 0
    self.assign_limit = assign_limit

  @cython.boundscheck(False)
  @cython.wraparound(False)
  def release(self):
    cdef list data = [
      self.pair_data[:self.pair_index, :], self.conv_data[:self.conv_index, :],
      self.div_data[:self.div_index, :], 
      # self.ind_data[:self.ind_index, :]
      self.ind_data[:self.ind_index, :assign_features.COUNT],
    ]
    self.pair_index = 0
    self.conv_index = 0
    self.div_index = 0
    self.ind_index = 0

    self.call_num = 0

    return data

  @cython.boundscheck(False)
  @cython.wraparound(False)
  def generate(self, score, chord, active_voices):
    self.call_num += 1

    cdef bint yield_true = active_voices.voiceid_type == "true"
    cdef float beat_horizon = active_voices.beat_horizon

    cdef list active_subset = active_voices.subset(chord)

    cdef int chord_len = len(chord)
    cdef int active_subset_len = len(active_subset)

    cdef list assignments
    cdef tuple assignment, voices

    cdef int voice_count, empty_count
    cdef int voice_index

    cdef int i

    note_features.create(self.all_note_data[:chord_len, :], chord, beat_horizon)
    voice_features.create(
      self.all_voice_data[:active_subset_len + 1, :], active_subset
    )
    pair_features.create(
      self.all_pair_data[:chord_len, :active_subset_len + 1, :], 
      chord, active_subset
    )

    # for note in chord:
    #   for i in range(note_features.COUNT):
    #     self.note_data[self.ind_index, i] += self.all_note_data[<int> note.index, i]
    #
    #   for i in range(note_features.COUNT):
    #     self.note_data[self.ind_index, i] /= chord_len

    for assignments in self.assignments_generator(
      chord, active_subset, yield_true
    ):
      for assignment in assignments:
        voice_count = 0
        empty_count = 0

        for note, voices in zip(chord, assignment):
          voice_count += len(voices)
          empty_count += voices[0] is None

          if voices[0] is None:
            assert len(voices) == 1

          for voice in voices:
            voice_index = active_subset_len if voice is None else voice.subset_index
            assert voice_index != -1, "subset index is -1"

            # for i in range(voice_features.COUNT):
            #   self.voice_data[self.ind_index, i] += self.all_voice_data[voice_index, i]

            self.pair_data[self.pair_index, :pair_features.COUNT] = (
              self.all_pair_data[<int> note.index, voice_index, :]
            )
            self.pair_data[
              self.pair_index, pair_features.COUNT : 
              pair_features.COUNT + note_features.COUNT
            ] = self.all_note_data[<int> note.index, :]
            self.pair_data[
              self.pair_index, pair_features.COUNT + note_features.COUNT:
            ] = self.all_voice_data[voice_index, :]

            self.pair_index += 1


        # for i in range(voice_features.COUNT):
        #   self.voice_data[self.ind_index, i] /= voice_count

        assert pair_features.PAD >= voice_count, voice_count

        for _ in range(pair_features.PAD - voice_count):
          self.pair_data[self.pair_index, :] = self.pair_data[self.pair_index - 1, :]
          self.pair_index += 1

        conv_features.create(
          self.conv_data[
            self.conv_index:self.conv_index + conv_features.PAD, :
          ],
          self.all_note_data[:chord_len, :],
          chord, assignment, beat_horizon
        )
        self.conv_index += conv_features.PAD

        div_features.create(
          self.div_data[self.div_index:self.div_index + div_features.PAD, :],
          self.all_voice_data[:active_subset_len + 1, :], chord, assignment
        )
        self.div_index += div_features.PAD

        assign_features.create(
          self.assign_data[self.ind_index, :],
          chord, assignment, voice_count, empty_count
        )
        self.ind_index += 1

      yield assignments

    cdef int pair_batch_len, conv_batch_len, div_batch_len, assign_batch_len
    if yield_true:
      pair_batch_len = self.assign_limit * pair_features.PAD * self.call_num
      conv_batch_len = self.assign_limit * conv_features.PAD * self.call_num
      div_batch_len = self.assign_limit * div_features.PAD * self.call_num
      ind_batch_len = self.assign_limit * self.call_num

      assert self.ind_index + self.assign_limit >= ind_batch_len + 1
      assert self.pair_index <= pair_batch_len

      assert (pair_batch_len - self.pair_index) % pair_features.PAD == 0
      for i in range(self.pair_index, pair_batch_len, pair_features.PAD):
        self.pair_data[i : i + pair_features.PAD, :] = (
          self.pair_data[i - pair_features.PAD : i, :]
        )
        self.pair_index += pair_features.PAD


      assert (conv_batch_len - self.conv_index) % conv_features.PAD == 0
      for i in range(self.conv_index, conv_batch_len, conv_features.PAD):
        self.conv_data[i : i + conv_features.PAD, :] = (
          self.conv_data[i - conv_features.PAD : i, :]
        )
        self.conv_index += conv_features.PAD

      assert (div_batch_len - self.div_index) % div_features.PAD == 0
      for i in range(self.div_index, div_batch_len, div_features.PAD):
        self.div_data[i : i + div_features.PAD, :] = (
          self.div_data[i - div_features.PAD : i, :]
        )
        self.div_index += div_features.PAD

      for i in range(self.ind_index, ind_batch_len):
        self.ind_data[i, :] = self.ind_data[i-1, :]
        self.ind_index += 1
