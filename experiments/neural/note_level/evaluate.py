from config import *
import voicesep as vs

if __name__ == '__main__':

  print("Reading Scores ...")
  scores =  [
    vs.Score(
      "%s%s.xml" % (score_path, score_name),
      bh, one_to_many
    )
    for score_name, bh in zip(score_list, beat_horizons)
  ]

  print("Compiling Network ...")
  network = vs.neural.note_level.NeuralNetwork(
    (vs.neural.note_level.Features.COUNT,) + hidden_dimensions + (1,),
    merge_layers,
    hidden_activations, output_activation,
    update_function, update_args, 
    l2_reg, mode
  )

  active_voices = vs.ActiveVoices(
    div_limit, lookback_inc, lookback_proxs, allow_overlap
  )
  features = vs.neural.note_level.Features()
  dataset = vs.neural.note_level.Dataset(dataset_file, "r")
  evaluator = vs.Evaluator(results_file, write_mode, header, "neural")

  for i in range(fold_start_i, fold_end_i, fold_size):
    train_scores = scores[:i] + scores[i+fold_size:]
    test_scores = scores[i:i+fold_size]

    network_file = "_".join(
      "".join(
        title if "bwv" in title else title[0] 
        for title in test_score.name.split("_")
      )
      for test_score in test_scores
    )

    try:
      network.read("%s%s" % (network_path, network_file))

    except FileNotFoundError:
      print("%d / %d - Training" % ((i // fold_size) + 1, fold_count))
      print(str([score.name for score in train_scores]), end="\n\n")

      dataset.read(train_scores)
      network.train(dataset, epochs, batch_size, network_cprint)
      network.write("%s%s" % (network_path, network_file))



    print("  Testing: %s" % str([score.name for score in test_scores]))
    for score in test_scores:
      vs.neural.note_level.separate(
        score, active_voices, features, network,
        conv_limit, div_limit, allow_cross, assignment_threshold
      )

      evaluator.update(score)
      _, _, JI, F1 = vs.Evaluator.jaccard_index(
        **vars(evaluator.results["all"][-1])
      )
      print("    Score: %s, JI-%f, F1-%f" % (score.name, JI, F1))

      if score.name in write_score:
        print("      Writing %s" % score.name)
        score.write("%s%s.xml" % (pred_scores, score.name), "neural")

    print()

  evaluator.total()
  evaluator.close()
