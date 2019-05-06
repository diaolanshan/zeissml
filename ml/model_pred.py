# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:38:38 2019

@author: WON4SZH
"""

import pickle
from builtins import print

import numpy as np
import pandas as pd


class Predict():
    def __init__(self):
        file = open(b"..\\model\\pipe_model.pkl", 'rb')
        self.model_file = pickle.load(file)
        file = open(b"..\\model\\prepare_pred.pkl", 'rb')
        self.data_prep_file = pickle.load(file)
        file.close()
        print('Model loaded.')

    def prepare_pred_data(v_list):
        colnames = ['X1_age', 'X2_gender', 'X3_edu', 'X4_Zeisis', 'X5_insurance', 'X6_qualification', 'X7_acquaintance',
                    'X8_shotsight', 'X9_income', 'X10_intemperance']
        colnames = np.array(colnames)
        dt_t = pd.DataFrame(np.array(v_list).reshape(1, 10), columns=colnames).replace({'无': '否'})
        return dt_t

    def pred_func(self, v_l):
        dt_pred = self.data_prep_file(v_l)

        self.model_file.predict(dt_pred)
        self.model_file.predict_proba(dt_pred)
        return [self.model_file.predict(dt_pred), self.model_file.predict_proba(dt_pred)]


v_l = [50, '男', '本科', '高', '有', '三甲', '有', '否', 1, '否']

pre = Predict()

print(pre.pred_func(v_l))

print(pre.pred_func(v_l))

print(pre.pred_func(v_l))
