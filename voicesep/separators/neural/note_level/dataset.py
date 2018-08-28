import h5py
import numpy as np
import theano

class Dataset:

  def __init__(self, data_file):
    
    self.fp = h5py.File("{}.hdf5".format(data_file), "r+")

  def read(self, score_names):

    feature_groups = [self.fp[name]["features"] for name in score_names]
    label_groups = [self.fp[name]["labels"] for name in score_names]

    features = Data(feature_groups)
    labels = Data(label_groups)

    return features, labels

  def write(self, score, active_voices, features):

    group = self.fp.create_group(score.name)

    features_dataset = group.create_dataset(
      name="features",
      shape=(0, features.COUNT),
      maxshape=(None, features.COUNT),
      dtype=theano.config.floatX
    )
    labels_dataset = group.create_dataset(
      name="labels",
      shape=(0,),
      maxshape=(None,),
      dtype=np.int16
    )

    assignments = score.separate()
    active_voices.update(assignments[0])
    length = 0
    for chord, assignment in zip(score[1:], assignments[1:]):
      active_subset = active_voices.subset(chord.beat_onset)

      data, labels = features.generate(chord, active_subset, get_labels=True)

      length += len(data)
      if features_dataset.len() <= length:
        features_dataset.resize((length * 2, features.COUNT))
        labels_dataset.resize((length * 2,))

      features_dataset[length - len(data):length] = data
      labels_dataset[length - len(data):length] = labels

      active_voices.update(assignment)

    features_dataset.resize((length, features.COUNT))
    labels_dataset.resize((length,))

class Data():

  def __init__(self, groups):
    
    self.groups = groups

    start = 0
    self.starts = [] 
    self.stops = []
    for group in groups:
      self.starts.append(start)
      self.stops.append(start + group.len())

      start += group.len()

    self.length = start

  def __getitem__(self, index):

    assert type(index) == "slice", "hello"

    start = index.start if index.start else 0
    stop = (
      index.stop 
      if index.stop and index.stop <= self.length
      else self.length
    )

    data = np.empty(
      (stop - start,) + self.shape[1]), dtype=theano.config.floatX
    )

    get_start = 0
    for group, start, stop in zip(self.groups, self.starts, self.stops):
      if start > indexstart or stop <= indexstop:
        continue

      mstart = max(0, indexstart - start)
      mstop = min(stop - start, indexstop - start)

      data[get_start : get_start + mstop - mstart] = (
          group[mstart:mstop]
      )

      get_start += mstop - mstart
      if get_start >= len(data):
        break

    return array

  def shape(self):
    return self.shape

  def __len__(self):
    return self.shape[0]
