# TODO List
#01 OK separate movies by genres
#02 OK get rating for each movide based on genre
#02.1 TODO debug 
#03 OK Create other reccomendation  by genre

# Local Import
import scripts.util as ut

# External Import
from operator import itemgetter


def make_user_genre_dict(target, user_genre_dict, content_dict):
  user_dict = {}
  for pair in target:
    count_genres = 0
    user, item = pair.split(',')
    if user not in user_dict: user_dict[user] = []
    genres = content_dict[item]['Genre'].split(', ')
    for genre in genres:
      # print(count_genres, genre, user_genre_dict[user].keys())
      if user in user_genre_dict: 
        count_genres += int(genre in user_genre_dict[user])
    user_dict[user].append([item,count_genres])
    user_dict[user] = sorted(user_dict[user], key=itemgetter(1), reverse=True)
  return user_dict

  
def make_recomendation_from_dict(dictionary):
  recomendations = []
  for user in dictionary:

    for item, importance in dictionary[user]:
       recomendations.append([user,item])

  with open(ut.RECOMENDATION, 'w') as recomendation_file:

    recomendation_file.writelines('UserId,ItemId\n')
    recomendation_file.writelines([value[0] +','+ value[1] + '\n' for value in recomendations])
  return recomendations

######################################

def make_movie_content_list(dictionary, key='imdbVotes', treat_coomma=False):
  movie_popularity = [[movie, dictionary[movie][key]] for movie in dictionary.keys() if dictionary[movie][key] != 'N/A' ]

  if treat_coomma: movie_popularity= [[item[0],int(item[1].replace(',',''))] for item in movie_popularity]
  movie_popularity = sorted(movie_popularity, key=itemgetter(1), reverse=True)
  return movie_popularity

def make_genre_dict(train_user_dict, content_dict):  
  genre_dict = {}
  for user_id in train_user_dict.keys():
    genre_dict[user_id] = {}
    items = train_user_dict[user_id]['Items']
    for item in items:
      genres = content_dict[item]['Genre'].split(', ')
      for genre in genres:
        if genre not in genre_dict[user_id]: genre_dict[user_id][genre] = []
        genre_dict[user_id][genre].append(item)
  return genre_dict

def rating_by_genre(user, item, ratings, content_dict, genre_dict):

  genre_count = 1
  rate_by_genre = 0
  genres = content_dict[item]['Genre'].split(',')
  for genre in genres:
    if not genre in genre_dict[user]: continue
    n_items = len(genre_dict[user][genre])
    genre_rating = 0 
    for genre_item in genre_dict[user][genre]:
      genre_rating += ratings[user + ':' + genre_item]['Rating']
    genre_rating = genre_rating/n_items
    rate_by_genre += genre_rating
    genre_count += 1
  
  return rate_by_genre, genre_count

def genre_prediction(train, targets, content_dict):
  train_user_dict, train_item_dict, train_ratings_dict = train
  genre_dict = make_genre_dict(train_user_dict, content_dict)

  mean_rating = 0
  for key in train[2]:
    mean_rating += train[2][key]['Rating']
  mean_rating = mean_rating/len(train[2])

  predictions = []
  for pair in targets:
    _tuser, _titem = pair.split(',')
    dif_item_mean = 0
    dif_rating = 0
    weight = 1
    if _titem in train_item_dict:
      _item_dict = train_item_dict[_titem]
      dif_item_mean = _item_dict['Rating_sum']/len(_item_dict['Users']) - mean_rating
    
      
      if _tuser in train_user_dict: 
        dif_rating, weight = rating_by_genre(_tuser, _titem, train_ratings_dict, 
                                              content_dict, genre_dict) 
        if dif_rating > 0: dif_rating = dif_rating - mean_rating
    
    prediction = mean_rating + (dif_rating + dif_item_mean)/(weight) 
    if prediction < 0: break
    predictions.append([_tuser, _titem, prediction])
  
  predictions = sorted(predictions, key=itemgetter(2), reverse=True)  
  predictions = sorted(predictions, key=itemgetter(0), reverse=False)
  return predictions


def genre_recomendation(train, targets, content_dict):
  predictions = genre_prediction(train, targets, content_dict)
  recomend_dict = {}
  
  for user, item, rating in predictions:

    if user not in recomend_dict: recomend_dict[user] = []
    recomend_dict[user].append(item)

  with open(ut.RECOMENDATION, 'w') as recomendation_file:
    recomendations = []
    for user in recomend_dict.keys():
      # [recomendations.append(user + ',' + item + '\n') for item in recomend_dict[user]]
      [recomendations.append(user + ',' + item) for item in recomend_dict[user]]
  
    recomendation_file.writelines('UserId,ItemId\n')
    recomendation_file.writelines(recomendations)
  return recomendations