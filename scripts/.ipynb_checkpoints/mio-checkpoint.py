#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
import json
import os
import math

from surprise.prediction_algorithms.matrix_factorization import SVD,SVDpp
from surprise.prediction_algorithms.knns import KNNWithZScore
from surprise.model_selection import train_test_split
from surprise import accuracy,Dataset, Reader
from surprise.model_selection import GridSearchCV

from util import *


# In[2]:


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


# In[ ]:


data,trainset,testset = get_data("data/ratings.jsonl")
model = KNNWithZScore()

#params = get_best_params(data,model)

algo = KNNWithZScore()#(n_epochs = params.n_epochs,n_factors = params.n_factors,lr_all = params.lr_all,reg_all = params.reg_all)
print("model loaded")

algo.fit(trainset)
print("training done")

predictions = algo.test(testset)
print("RMSE do modelo ",accuracy.rmse(predictions),sep='')


# In[ ]:


build_final_predictions("data/targets.csv")
print("submission done")


# In[ ]:




