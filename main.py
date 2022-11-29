
# Local Imports 
import scripts.util as ut
import recomender.content_based as cbased
import recomender.ensamble as ensamble

# External Imports
import sys


program, ratings, contents, target_file = sys.argv

# Read Targets
with open(target_file, 'r') as targets_file:
  targets_file.readline()
  targets = targets_file.readlines()

targets = [target[:-1] for target in targets]

# Read Content
content_dict = ut.read_content(contents)

# Separate test and train
test, train = ut.read_ratings(ratings, test_size=0)

# put test in the same recomendation format
test_recomendation = eval.test_to_recomendation(test)

# Run Ensamble and return dict
ensamble_recommend_dict = ensamble.ensamble1(train, targets, content_dict, vote_strengh=50)

# Make recomendation from dict
recomendation = cbased.make_recomendation_from_dict(ensamble_recommend_dict)