#TODO LIST
#01 OK Trivial Prediction
#02 OK Trivial Recommendation


# Local Import
import util as ut

# External Import
from operator import itemgetter


def trivial_prediction(train, targets):
  # rating_keys = train[2].keys()
  train_user_dict, train_item_dict, train_ratings_dict = train
  

  mean_rating = 0
  for key in train[2]:
    mean_rating += train[2][key]['Rating']
  mean_rating = mean_rating/len(train[2])



  predictions = []
  for pair in targets:
    _tuser, _titem = pair.split(":")
    if _titem in train_item_dict:
      _item_dict = train_item_dict[_titem]
      prediction = _item_dict['Rating_sum']/len(_item_dict['Users'])
    else:
      prediction = mean_rating
    predictions.append([_tuser, _titem, prediction])
  
  predictions = sorted(predictions, key=itemgetter(2), reverse=True)  
  return predictions



  
def trivial_recomendation(train, targets):
  predictions = trivial_prediction(train, targets)
  recomend_dict = {}
  
  for user, item, rating in predictions:

    if user not in recomend_dict: recomend_dict[user] = []
    recomend_dict[user].append(item)

  with open(ut.RECOMENDATION, 'w') as recomendation_file:
    recomendations = []
    for user in recomend_dict.keys():
      [recomendations.append(user + ':' + item + '\n') for item in recomend_dict[user]]
  
    recomendation_file.writelines('UserId:ItemId\n')
    recomendation_file.writelines(recomendations)
  return recomendations