# TODO LIST
#01 TODO read json
#02 TODO default output

# Local Imports 
import util as ut
import recommender.trivial as triv

# External Imports
import json

import numpy as np
import pandas as pd
import json
import os
import math

from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy,Dataset, Reader
from surprise.model_selection import GridSearchCV

from util import round_closest,get_data,get_best_params,build_final_predictions

jsonObj = pd.read_json(path_or_buf=path,lines=True)
jsonObj['Timestamp'] = pd.to_datetime(jsonObj['Timestamp']).astype(int)/ 10**9
jsonObj['Timestamp'] = jsonObj['Timestamp']/(10**9)



reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(jsonObj[['UserId', 'ItemId','Rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)
    

algo = SVD()

algo.fit(trainset)
predictions = algo.test(testset)

#print(accuracy.rmse(predictions))

build_final_predictions("targets.csv")