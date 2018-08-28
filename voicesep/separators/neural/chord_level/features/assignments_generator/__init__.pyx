#cython: language_level=3
import cython

cdef class AssignmentsGenerator:
  def __cinit__(
    self, size_t max_rows, size_t assign_limit, size_t random_limit,
    size_t conv_limit, size_t div_limit, size_t pp_limit,
    bint lookback, bint allow_cross
  ):
    assert max_rows >= assign_limit

    self.max_rows = max_rows
    self.assign_limit = assign_limit

    self.assignments = [None] * <unsigned> self.max_rows

    self.thisptr = new CAssignmentsGenerator(
      max_rows, assign_limit, random_limit,
      conv_limit, div_limit, pp_limit,
      lookback, allow_cross
    )

  def __dealloc__(self):
    if self.thisptr != NULL:
      del self.thisptr

  @cython.boundscheck(False)
  @cython.wraparound(False)
  def __call__(self, chord, list active_subset, bint yield_true, bint test_all=False):
    cdef size_t i = 0, j = 0, k = 0
    cdef size_t repeat_index = 0

    cdef size_t chord_len = len(chord)
    cdef size_t active_subset_len = len(active_subset)

    cdef vector[Note] vchord
    vchord.resize(chord_len)
    for i in range(chord_len):
      vchord[i].pitch_space = chord[i].pitch_space

      vchord[i].repeat_index = -1
      vchord[i].poly_above = 100
      vchord[i].poly_below = -1
      if chord[i].repeat_behind and chord[i].repeat_count > 4:
        for j in range(active_subset_len):
          if active_subset[j].note is chord[i].repeat_behind:
            repeat_index = j
            break
        vchord[i].repeat_index = repeat_index
      else:
        for j in range(active_subset_len):
          if (
            active_subset[j].note.repeat_ahead and 
            active_subset[j].note.repeat_count > 4
          ):
            if active_subset[j].note.pitch_space < chord[i].pitch_space:
              vchord[i].poly_above = j
            else:
              vchord[i].poly_below = j
            break

      

    cdef vector[Voice] vactive_subset
    vactive_subset.resize(active_subset_len)
    for i in range(active_subset_len):
      vactive_subset[i].pitch_space = active_subset[i].pitch_space
      vactive_subset[i].div_count = active_subset[i].div_count
      vactive_subset[i].position = active_subset[i].position
      vactive_subset[i].lookback_prox = active_subset[i].lookback_prox

    cdef size_t row = 0
    cdef size_t true_size = 0
    cdef vector[vector[int]] true_assignment
    if yield_true:
      for note in chord:
        note.true_pairs.left.sort(key=lambda p : active_subset.index(p))

      true_assignment.resize(chord_len)
      true_size = chord_len
      for i, note in enumerate(chord):
        if len(note.true_pairs.left) == 0:
          true_assignment[i].push_back(-1)
        else:
          for p in note.true_pairs.left:
            true_assignment[i].push_back(active_subset.index(p))

      self.assignments[0] = tuple(
        tuple(
          active_subset[true_assignment[i][j]] if
          true_assignment[i][j] > -1 else None
          for j in range(true_assignment[i].size())
        )
        for i in range(chord_len)
      )
      row += 1

    cdef size_t assign_count = 0
    self.thisptr.init_generator()
    while self.thisptr.generating():
      assign_count = self.thisptr[0](vchord, vactive_subset, (not yield_true or test_all))
      for i in range(assign_count):
        if true_size > 0:
          for j in range(chord_len):
            if true_assignment[j].size() != self.thisptr.assignments[i][j].size():
              break

            for k in range(true_assignment[j].size()):
              if true_assignment[j][k] == self.thisptr.assignments[i][j][k]:
                continue

              break
            else:
              continue

            break
          else:
            true_size = 0
            continue

        self.assignments[row] = tuple(
          tuple(
            active_subset[<unsigned> self.thisptr.assignments[i][j][k]] if
            self.thisptr.assignments[i][j][k] > -1 else None
            for k in range(self.thisptr.assignments[i][j].size())
          )
          for j in range(chord_len)
        )
        row += 1

        if row == self.max_rows:
          yield self.assignments[:row]
          row = 0

    if row > 0:
      assert row <= self.max_rows
      if yield_true and not test_all:
        assert row <= self.assign_limit + 1
        if row == self.assign_limit + 1:
          yield self.assignments[:self.assign_limit]
        else:
          yield self.assignments[:row]
      else:
        yield self.assignments[:row]
