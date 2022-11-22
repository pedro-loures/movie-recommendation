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

data,trainset,testset = get_data("ratings.jsonl")
model = SVD()

#params = get_best_params(data,model)

algo = SVD()#(n_epochs = params.n_epochs,n_factors = params.n_factors,lr_all = params.lr_all,reg_all = params.reg_all)

algo.fit(trainset)
predictions = algo.test(testset)

#print(accuracy.rmse(predictions))

build_final_predictions("targets.csv")