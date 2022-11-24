#TODO LIST
#01 OK evaluate via metric that will be used in TP
#02 TODO evaluate via other metrics

# External Imports
import numpy as np
from sklearn.metrics import ndcg_score
from operator import itemgetter


def test_to_recomendation(test):
  test_user_dict, test_item_dict, test_ratings_dict = test
  
  ratings = []
  for key in test_ratings_dict.keys():
    ratings.append([key, test_ratings_dict[key]['Rating']] )
    
  ratings = sorted(ratings, key=itemgetter(1), reverse=True)
  
  user_dict = {}
  for pair, rating in ratings:
    user, item = pair.split(':')
    if user not in user_dict: user_dict[user] = []
    user_dict[user].append(item)
  recomendations = []
  for user in user_dict.keys():
    [recomendations.append(user + ',' + item + '\n') for item in user_dict[user]]
  
  return recomendations



def get_relevance(recomendation, expected):
  expected_dict = {}
  recomendation_dict = {}

  # Create dict with user item and true relevance
  user_relevance = {}
  for pair in expected:
    user, item = pair[:-1].split(',')
    if user not in expected_dict: 
      expected_dict[user] = []
      user_relevance[user] = 0
    user_relevance[user] += 1
    expected_dict[user].append([item, user_relevance[user]])
    
  # create a dict with the pairs and relevance in relation to the user
  user_relevance = {}
  for pair in recomendation:
    pair = pair[:-1]
    user, item = pair.split(',')
    if user not in user_relevance: user_relevance[user] = 0
    user_relevance[user] += 1
    
    recomendation_dict[pair] = user_relevance[user]
    
  # match the order of the true relevance to the predicted relevance
  true_relevance = []
  expected_relevance = []
  for user in expected_dict.keys():
    for item_relevance in expected_dict[user]:
      item, relevance = item_relevance
      true_relevance.append(relevance)
      expected_relevance.append(recomendation_dict[user + ',' + item])      




  return true_relevance, expected_relevance

def discount_cumulative_gain(recomendation, expected):
  true_relevance, expected_relevance = get_relevance(recomendation, expected)
  
  return ndcg_score(np.array([true_relevance]), np.array([expected_relevance]))
