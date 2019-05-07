import pickle
from builtins import print
import pandas as pd

class Predict():
    def __init__(self):
        file = open(b".\\model\\pipe_model.pkl", 'rb')
        self.model_file = pickle.load(file)
        file.close()
        print('Model loaded.')

    def prepare_pred_data(self, v_list):
        import numpy as np
        colnames = ['X1_age', 'X2_gender', 'X3_edu', 'X4_Zeisis', 'X5_insurance', 'X6_qualification', 'X7_acquaintance',
                    'X8_shotsight', 'X9_income', 'X10_intemperance']
        colnames = np.array(colnames)
        dt_t = pd.DataFrame(np.array(v_list).reshape(1, 10), columns=colnames).replace({'无': '否'})
        return dt_t

    def pred_func(self, v_l):
        dt_pred = self.prepare_pred_data(v_l)

        self.model_file.predict(dt_pred)
        self.model_file.predict_proba(dt_pred)
        return [self.model_file.predict(dt_pred), self.model_file.predict_proba(dt_pred)]