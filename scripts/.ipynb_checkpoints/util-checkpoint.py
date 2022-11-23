
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