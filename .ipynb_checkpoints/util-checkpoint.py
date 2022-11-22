
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
TARGETS = DATA_PATH + "targets.jsonl"

# Output paths 
RECOMENDATION = "results\\recommendations.txt"


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