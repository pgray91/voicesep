import h5py
import numpy as np
import theano

class Dataset:
  def __init__(self, data_file, mode):
    self.fp = h5py.File("%s.hdf5" % data_file, mode)

    self.score_count = 0
    self.features = None
    self.labels = None

  def close(self):
    self.fp.close()

  def read(self, score_list):
    self.score_count = len(score_list)

    self.features = MemMaps(self.fp, score_list, "features")
    self.labels = MemMaps(self.fp, score_list, "labels")

  def write(self, score, active_voices, features):
    active_voices.voiceid_type = "true"
    active_voices.beat_horizon = score.beat_horizon

    if "feature_count" not in self.fp.attrs:
      self.fp.attrs["feature_count"] = features.COUNT

    group = self.fp.create_group(score.name)

    features_fp = group.create_dataset(
      "features", (0, features.COUNT), 
      maxshape=(None, features.COUNT),
      dtype=theano.config.floatX
    )
    labels_fp = group.create_dataset(
      "labels", (0,), 
      maxshape=(None,),
      dtype=np.int16
    )

    data_len = 0
    active_voices.update(score[0])
    for chord in score[1:]:
      active_voices.filter(chord.beat_onset)

      data, labels = features.generate(chord, active_voices, get_labels=True)

      prev_data_len = data_len
      data_len += len(data)
      if features_fp.len() <= data_len:
        features_fp.resize((data_len * 2, features.COUNT))
        labels_fp.resize((data_len * 2,))

      features_fp[prev_data_len:data_len] = data
      labels_fp[prev_data_len:data_len] = labels

      active_voices.update(chord)

    features_fp.resize((data_len, features.COUNT))
    labels_fp.resize((data_len,))

    active_voices.clear()

class MemMaps():
  def __init__(self, fp, score_list, set_id):
    self.fp = fp
    self.set_id = set_id

    self.memmaps = [None] * len(score_list)
    start = 0
    for i, score in enumerate(score_list):
      length = fp[score.name][set_id].len()
      self.memmaps[i] = MemMap(
        path = "%s/%s" % (score.name, set_id),
        start = start,
        stop = start + length,
        length = length
      )
      start += length

    if set_id != "labels":
      self.shape = (start, self.fp.attrs["feature_count"])
    else:
      self.shape = (start,)

  def __getitem__(self, index):
    start = index.start if index.start else 0
    stop = (
      index.stop 
      if index.stop and index.stop <= self.shape[0] 
      else self.shape[0]
    )

    if self.set_id != "labels":
      get_array = np.empty(
        (stop - start, self.shape[1]), dtype=theano.config.floatX
      )
    else:
      get_array = np.empty((stop - start,), dtype=theano.config.floatX)

    get_start = 0
    i = self.memmaps.index(start)
    while True:
      memmap = self.memmaps[i]

      mstart = start - memmap.start 
      if mstart < 0:
        mstart = 0

      mstop = stop - memmap.start 
      if mstop > memmap.length:
        mstop = memmap.length

      get_array[get_start : get_start + mstop - mstart] = (
        self.fp[memmap.path][mstart:mstop]
      )

      get_start += mstop - mstart
      if get_start >= len(get_array):
        break

      i += 1

    return get_array

  def shape(self):
    return self.shape

  def __len__(self):
    return self.shape[0]

class MemMap():
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __eq__(self, index):
    return self.start <= index and self.stop > index
