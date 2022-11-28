# TODO List 
# OK Based on database popularity
# TODO Based on imdb Votes


# Local Import
import scripts.util as ut

# External Import
from operator import itemgetter


# def create_user_dict(target):
#   user_dict = {}
#   for pair in target:
    
#     user, item = pair.split(',')
#     if user not in user_dict: user_dict[user] = []
#     user_dict[user].append(item)
#   return user_dict




def make_popularity_list(dictionary, key='Users'):
  movie_popularity = [[movie, len(dictionary[movie][key])] for movie in dictionary.keys()]
  movie_popularity = sorted(movie_popularity, key=itemgetter(1), reverse=True)

  return movie_popularity



def recomend_popular(train, target, movie_popularity_list):

  train_user_dict, train_item_dict, train_ratings_dict = train

  movie_popularity = {}

  for movie, popularity in movie_popularity_list:
    movie_popularity[movie]=popularity

  user_dict = ut.create_user_dict(target)

  recomendations = []
  for user in user_dict.keys():
    
    user_recommendations = []
    for target in user_dict[user]:
      user_recommendations.append([target,0])
      if target in movie_popularity: user_recommendations[-1] = [target,movie_popularity[target]]
    

    user_recommendations = sorted(user_recommendations, key=itemgetter(1), reverse=True)
    [recomendations.append([user , *movie]) for movie in user_recommendations]
  recomendations = sorted(recomendations, key=itemgetter(0), reverse=False)


  with open(ut.RECOMENDATION, 'w') as recomendation_file:
    recomendations_text = [item[0] + ',' + item[1] +'\n' for item in recomendations]
  
    recomendation_file.writelines('UserId,ItemId\n')
    recomendation_file.writelines(recomendations_text)
        
  return recomendations_text