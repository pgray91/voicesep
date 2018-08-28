import voicesep as vs

# Score
beat_horizon=10000
one_to_many=True

div_limit = 0
lookback_inc = 1
lookback_proxs = (100,)
allow_overlap = True

results_file="results"
header = ""

# Corpus
pop_path= "../../voicesep/corpus/pop/"
pop_list=[
  ("21_guns", beat_horizon, False),
  ("apples_to_the_core", beat_horizon, False),
  ("count_on_me", beat_horizon, False),
  ("dreams", beat_horizon, False),
  ("earth_song", beat_horizon, False),
  ("endless_love", beat_horizon, False),
  ("forest", beat_horizon, False),
  ("fur_elise", beat_horizon, False),
  ("greensleeves", beat_horizon, False),
  ("how_to_save_a_life", beat_horizon, False),
  ("hymn_for_the_weekend", beat_horizon, False),
  ("knocking_on_heavens_door", beat_horizon, False),
  ("let_it_be", beat_horizon, False),
  ("one_call_away", beat_horizon, False),
  ("see_you_again", beat_horizon, False),
  ("teenagers", beat_horizon, False),
  ("thousand_miles", beat_horizon, False),
  ("to_a_wild_rose", beat_horizon, False),
  ("uptown_girl", beat_horizon, False),
  ("when_i_look_at_you", beat_horizon, False),
]

chorale_path= "../../voicesep/corpus/chorales/"
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


# score_path=pop_path
# score_list=pop_list

score_path=chorale_path
score_list=chorale_list

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
