from libcpp.vector cimport vector
cdef extern from "cassignments_generator.h":
  struct Note:
    int pitch_space
    int repeat_index
    int poly_above
    int poly_below

  struct Voice:
    int pitch_space
    int div_count
    int position
    int lookback_prox

  cdef cppclass CAssignmentsGenerator:
    CAssignmentsGenerator (
      size_t max_rows, size_t assign_limit, size_t random_limit,
      size_t conv_limit, size_t div_limit, size_t pp_limit, 
      bint lookback, bint allow_cross
    )

    void init_generator();
    bint generating();
    size_t operator()(
      vector[Note]& chord, vector[Voice]& active_subset, bint get_all
    )
    vector[vector[vector[int]]] assignments

cdef class AssignmentsGenerator:
  cdef:
    list assignments

    readonly size_t max_rows
    readonly size_t assign_limit
    CAssignmentsGenerator *thisptr
