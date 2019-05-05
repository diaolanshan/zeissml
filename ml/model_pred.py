# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:38:38 2019

@author: WON4SZH
"""

import pickle

file = open(b"D:\\Spyder\\BOSCH\\project_eric\\model\\pipe_model.pkl", 'rb')
model_file = pickle.load(file)
file = open(b"D:\\Spyder\\BOSCH\\project_eric\\model\\prepare_pred.pkl", 'rb')
data_prep_file = pickle.load(file)
file.close()

v_l = [50, '男', '本科', '高', '有', '三甲', '有', '是', 48, '否']


def pred_func(v_l):
    dt_pred = data_prep_file(v_l)

    model_file.predict(dt_pred)
    model_file.predict_proba(dt_pred)
    return [model_file.predict(dt_pred), model_file.predict_proba(dt_pred)]


pred_func(v_l)
