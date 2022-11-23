
# TODO LIST
#01 TODO data reader
#02 TODO Divide test and train

import numpy as np
import pandas as pd
import json
import os
import math

from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy,Dataset, Reader
from surprise.model_selection import GridSearchCV



# Debug
debug_text = "test text"

# Input paths (change data to your path)
DATA_PATH = "C:\\Users\\PLour\\OneDrive - Universidade Federal de Minas Gerais\\01_Estudos\\Faculdade\\RS\\RC2\\data\\data\\"
RATINGS = DATA_PATH + "ratings.jsonl"
CONTENT = DATA_PATH + "content.jsonl"
TARGETS = DATA_PATH + "targets.csv"

# Output paths 
RECOMENDATION = "results\\submission.csv"


#data = ut.get_data(ut.RATINGS)


# Read Ratings and return test and train dicts
def read_ratings(test_size=0.33):
    test_size += 0.01

    with open(RATINGS, 'r') as json_file:
        json_list = list(json_file)

    # Test Dict
    test_user_dict = {}
    test_user_idx=0
    test_item_dict = {}
    test_item_idx=0
    test_ratings_dict = {}
    
    # Train Dict
    train_user_dict = {}
    train_user_idx=0
    train_item_dict = {}
    train_ratings_dict = {}
    train_item_idx=0

    counter = 1
    for json_str in json_list:
        result = json.loads(json_str)
        if (not isinstance(result, dict)):
            continue
        # print(counter, test_size, counter * test_size)
        item_id = result['ItemId']
        user_id = result['UserId']
        rating  = result['Rating']
        if counter * test_size > 1:
            counter = 0
            
            if item_id not in test_item_dict: 
                test_item_dict[item_id] = {'Idx':test_item_idx, 'Rating_sum':0, 'Users':[]}
                test_item_idx += 1
            test_item_dict[item_id]['Rating_sum'] += rating
            test_item_dict[item_id]['Users'].append(user_id)
            if user_id not in test_user_dict:
                test_user_dict[user_id] = {'Idx':test_user_idx, 'Rating_sum':0, 'Items':[]}
                test_user_idx += 1
            test_user_dict[user_id]['Rating_sum'] += rating
            test_user_dict[user_id]['Items'].append(item_id) 

            test_ratings_dict[user_id + ':' + item_id] = {'Timestamp':result['Timestamp'], 'Rating':rating}
        else:
            counter += 1
            if item_id not in train_item_dict: 
                train_item_dict[item_id] = {'Idx':train_item_idx, 'Rating_sum':0, 'Users':[]}
                train_item_idx += 1
            train_item_dict[item_id]['Rating_sum'] += rating
            train_item_dict[item_id]['Users'].append(user_id)
            if user_id not in train_user_dict:
                train_user_dict[user_id] = {'Idx':train_user_idx, 'Rating_sum':0, 'Items':[]}
                train_user_idx += 1
            train_user_dict[user_id]['Rating_sum'] += rating
            train_user_dict[user_id]['Items'].append(item_id) 
            train_ratings_dict[user_id + ':' + item_id] = {'Timestamp':result['Timestamp'], 'Rating':rating}

    return [test_user_dict, test_item_dict, test_ratings_dict], [train_user_dict, train_item_dict, train_ratings_dict]



def round_closest(x):
    y = math.floor(x)
    if x - y >= 0.5:
        return math.ceil(x)
    else:
        return y
    
def get_data(path):
    
    jsonObj = pd.read_json(path_or_buf=path,lines=True)
    #jsonObj['Timestamp'] = pd.to_datetime(jsonObj['Timestamp']).astype(int)/ 10**9
    #jsonObj['Timestamp'] = jsonObj['Timestamp']/(10**9)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(jsonObj[['UserId', 'ItemId','Rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    
    return data,trainset, testset

def get_best_params(data,model):
    param_grid = {"n_epochs": [20, 40], "n_factors":[100,200] , "lr_all": [0.002, 0.005], "reg_all": [0.4, 0.6]}
    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)

    gs.fit(data)
    params = gs.best_params["rmse"]

    with open('params.txt', 'w') as convert_file:
        convert_file.write(json.dumps(params))
    
    return params

def build_final_predictions(path):
    targets = pd.read_csv(path)
    targets["Rating"] = np.zeros(len(targets))
    targets = targets.to_numpy()

    predictions = algo.test(targets)
    predictions_list = [[tup.uid,tup.iid,tup.est] for tup in predictions]
    predictions_list = pd.DataFrame(data=predictions_list,columns=['UserId', 'ItemId','Rating'])
    predictions_list = predictions_list.sort_values(['UserId', 'Rating'], ascending=[True, False])
    ratings = predictions_list["Rating"]
    predictions_list = predictions_list.drop("Rating",axis=1)

    predictions_list.to_csv("sub.csv",index=False)