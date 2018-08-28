import voicesep as vs

# Global
output_dir="output/"

# Score
beat_horizon=4
one_to_many=True

# Features
data_file=output_dir + "features"

max_rows=800
assign_limit=800
random_limit=1200

conv_limit=2
div_limit=2
pp_limit=28

allow_cross=True
allow_overlap=True
lookback_inc=0.4
lookback_proxs=(7,1,-1)

# Network
network_dir=output_dir + "networks/"
mode="FAST_RUN"
network_cprint=10
testing_cprint=20

field_sizes = (50, 50, 50)
ind_layer = 0
hidden_dimensions=(50, )
merge_layers=(False, )
conv_activation="sigmoid"
hidden_activations="sigmoid"
output_activation=None

margin=1.0
l2_reg=0.001
rho=0.95
epsilon=1e-6

epochs=6
batch_size=20

update_function = vs.utils.gradients.adadelta
update_args = {
  "rho" : rho,
  "epsilon" : epsilon
}

# Cross Validation
fold_count=10
fold_start=0
fold_test_count=0

# Corpus
pred_scores=output_dir + "scores/vs_"

pop_path= "../../../voicesep/corpus/pop/"
pop_list=[
  ("count_on_me", beat_horizon, False),
  ("21_guns", beat_horizon, False),
  ("forest", beat_horizon, False),
  ("endless_love", beat_horizon, False),
  ("when_i_look_at_you", 6, False),
  ("greensleeves", beat_horizon, False),
  ("dreams", beat_horizon, False),
  ("earth_song", beat_horizon, False),
  ("how_to_save_a_life", beat_horizon, False),
  ("knocking_on_heavens_door", beat_horizon, False),
  ("apples_to_the_core", beat_horizon, False),
  ("teenagers", beat_horizon, False),
  ("fur_elise", beat_horizon, False),
  ("hymn_for_the_weekend", beat_horizon, False),
  ("let_it_be", beat_horizon, False),
  ("one_call_away", beat_horizon, False),
  ("see_you_again", beat_horizon, False),
  ("thousand_miles", beat_horizon, False),
  ("to_a_wild_rose", beat_horizon, False),
  ("uptown_girl", beat_horizon, False),
]

chorale_path= "../../../voicesep/corpus/chorales/"
chorale_list=[
  ("bwv250", beat_horizon, False),
  ("bwv251", beat_horizon, False),
  ("bwv252", beat_horizon, False),
  ("bwv253", beat_horizon, False),
  ("bwv254", beat_horizon, False),
  ("bwv255", beat_horizon, False),
  ("bwv256", beat_horizon, False),
  ("bwv257", beat_horizon, False),
  ("bwv258", beat_horizon, False),
  ("bwv259", beat_horizon, False),
  ("bwv260", beat_horizon, False),
  ("bwv261", beat_horizon, False),
  ("bwv262", beat_horizon, False),
  ("bwv263", beat_horizon, False),
  ("bwv264", beat_horizon, False),
  ("bwv265", beat_horizon, False),
  ("bwv266", beat_horizon, False),
  ("bwv267", beat_horizon, False),
  ("bwv268", beat_horizon, False),
  ("bwv269", beat_horizon, False),
  ("bwv270", beat_horizon, False),
  ("bwv271", beat_horizon, False),
  ("bwv272", beat_horizon, False),
  ("bwv273", beat_horizon, False),
  ("bwv276", beat_horizon, False),
  ("bwv277", beat_horizon, False),
  ("bwv278", beat_horizon, False),
  ("bwv279", beat_horizon, False),
  ("bwv280", beat_horizon, False),
  ("bwv281", beat_horizon, False),
  ("bwv282", beat_horizon, False),
  ("bwv283", beat_horizon, False),
  ("bwv284", beat_horizon, False),
  ("bwv285", beat_horizon, False),
  ("bwv286", beat_horizon, False),
  ("bwv287", beat_horizon, False),
  ("bwv288", beat_horizon, False),
  ("bwv289", beat_horizon, False),
  ("bwv290", beat_horizon, False),
  ("bwv291", beat_horizon, False),
  ("bwv292", beat_horizon, False),
  ("bwv293", beat_horizon, False),
  ("bwv294", beat_horizon, False),
  ("bwv295", beat_horizon, False),
  ("bwv296", beat_horizon, False),
  ("bwv297", beat_horizon, False),
  ("bwv298", beat_horizon, False),
  ("bwv299", beat_horizon, False),
  ("bwv300", beat_horizon, False),
  ("bwv301", beat_horizon, False),
]

fugue_path= "../../../voicesep/corpus/fugues/"
fugue_list=[
  ("bwv772", beat_horizon, False),
  ("bwv773", beat_horizon, False),
  ("bwv774", beat_horizon, False),
  ("bwv775", beat_horizon, False),
  ("bwv776", beat_horizon, False),
  ("bwv777", beat_horizon, False),
  ("bwv778", beat_horizon, False),
  ("bwv779", beat_horizon, False),
  ("bwv780", beat_horizon, False),
  ("bwv781", beat_horizon, False),
  ("bwv782", beat_horizon, False),
  ("bwv783", beat_horizon, False),
  ("bwv784", beat_horizon, False),
  ("bwv785", beat_horizon, False),
  ("bwv786", beat_horizon, False),
  ("bwv787", beat_horizon, False),
  ("bwv788", beat_horizon, False),
  ("bwv789", beat_horizon, False),
  ("bwv790", beat_horizon, False),
  ("bwv791", beat_horizon, False),
  ("bwv792", beat_horizon, False),
  ("bwv793", beat_horizon, False),
  ("bwv794", beat_horizon, False),
  ("bwv795", beat_horizon, False),
  ("bwv796", beat_horizon, False),
  ("bwv797", beat_horizon, False),
  ("bwv798", beat_horizon, False),
  ("bwv799", beat_horizon, False),
  ("bwv800", beat_horizon, False),
  ("bwv801", beat_horizon, False),
  ("bwv846", beat_horizon, False),
  ("bwv847", beat_horizon, False),
  ("bwv848", beat_horizon, False),
  ("bwv849", beat_horizon, False),
  ("bwv850", beat_horizon, False),
  ("bwv851", beat_horizon, False),
  ("bwv852", beat_horizon, False),
  ("bwv853", beat_horizon, False),
  ("bwv854", beat_horizon, False),
  ("bwv855", beat_horizon, False),
  ("bwv856", beat_horizon, False),
  ("bwv857", beat_horizon, False),
  ("bwv858", beat_horizon, False),
  ("bwv859", beat_horizon, False),
  ("bwv860", beat_horizon, False),
  ("bwv861", beat_horizon, False),
  ("bwv862", beat_horizon, False),
  ("bwv863", beat_horizon, False),
  ("bwv864", beat_horizon, False),
  ("bwv865", beat_horizon, False),
  ("bwv866", beat_horizon, False),
  ("bwv867", beat_horizon, False),
  ("bwv868", beat_horizon, False),
  ("bwv869", beat_horizon, False),
  ("bwv870", beat_horizon, False),
  ("bwv871", beat_horizon, False),
  ("bwv872", beat_horizon, False),
  ("bwv873", beat_horizon, False),
  ("bwv874", beat_horizon, False),
  ("bwv875", beat_horizon, False),
  ("bwv876", beat_horizon, False),
  ("bwv877", beat_horizon, False),
  ("bwv878", beat_horizon, False),
  ("bwv879", beat_horizon, False),
  ("bwv880", beat_horizon, False),
  ("bwv881", beat_horizon, False),
  ("bwv882", beat_horizon, False),
  ("bwv883", beat_horizon, False),
  ("bwv884", beat_horizon, False),
  ("bwv885", beat_horizon, False),
  ("bwv886", beat_horizon, False),
  ("bwv887", beat_horizon, False),
  ("bwv888", beat_horizon, False),
  ("bwv889", beat_horizon, False),
  ("bwv890", beat_horizon, False),
  ("bwv891", beat_horizon, False),
  ("bwv892", beat_horizon, False),
  ("bwv893", beat_horizon, False)
]

fugue_subset_list=[
  ("bwv846", beat_horizon, False),
  ("bwv847", beat_horizon, False),
  ("bwv848", beat_horizon, False),
  ("bwv850", beat_horizon, False),
  ("bwv851", beat_horizon, False),
  ("bwv852", beat_horizon, False),
  ("bwv853", beat_horizon, False),
  ("bwv857", beat_horizon, False),
  ("bwv859", beat_horizon, False),
  ("bwv861", beat_horizon, False),
]

# score_path=pop_path
# score_list=pop_list
# network_path=network_dir + "pop/"
# results_file=output_dir + "pop_results"

score_path=chorale_path
score_list=chorale_list
network_path=network_dir + "chorales/"
results_file=output_dir + "chorales_results"

# score_path=fugue_path
# score_list=fugue_list
# network_path=network_dir + "fugues/"
# results_file=output_dir + "fugues_results"

# score_path=fugue_path
# score_list=fugue_subset_list
# network_path=network_dir + "fugues_subset/"
# results_file=output_dir + "subset_results"

write_mode="a"
header = (
  "Conv=%d, Div=%d, Assign Limit=%d,"
  " Allow Overlap=%d, Epochs=%d, Batch Size=%d,"
  " Field Sizes=%s, Hidden Dimensions=%s,"
  " l2 reg=%f" % (
    conv_limit, div_limit, assign_limit, allow_overlap,
    epochs, batch_size,
    str(field_sizes), str(hidden_dimensions),
    l2_reg
  )
)

write_score=[
  item[0] for item in score_list if item[-1]
]
score_list=[
  item[:2] for item in score_list
]

beat_horizons=[
  item[1] for item in score_list
]
score_list=[
  item[0] for item in score_list
]

fold_size = (len(score_list) - 1) // fold_count + 1 
fold_start_i = fold_start * fold_size
fold_end_i = len(score_list)
if (
  fold_test_count > 0 and 
  fold_test_count + fold_start < fold_count
):
  fold_end_i = (fold_test_count + fold_start) * fold_size
