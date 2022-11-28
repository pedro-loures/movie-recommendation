import recomender.content_based as cbased

from operator import itemgetter


def ensamble1(train, target, content_dict, vote_strengh=2):
  user_genre_dict = cbased.make_genre_dict(train[0], content_dict)
  user_dict = cbased.make_user_genre_dict(target, user_genre_dict, content_dict)  
  movie_vote_list = cbased.make_movie_content_list(content_dict, treat_coomma=True)

  movie_vote_dict = {}
  for movie, note in movie_vote_list:
    if movie == '04eb8705ce': print ('aaaa')
    movie_vote_dict[movie] = note

  ensamble_dict = {}

  users = sorted(user_dict.keys())

  for user in users:
    ensamble_dict[user] = []
    for movie, weight in user_dict[user]:
      new_weight = weight 
      if movie in movie_vote_dict:
        new_weight += movie_vote_dict[movie] * vote_strengh
        new_weight = new_weight / (vote_strengh + 1) 

      ensamble_dict[user].append([movie, new_weight])
    ensamble_dict[user] = sorted(ensamble_dict[user], key=itemgetter(1), reverse=True)


  return ensamble_dict