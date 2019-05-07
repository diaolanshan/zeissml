import flask_login
from flask import request, render_template
from . import learning
from learning.model_pred import Predict
from decimal import *

predict = Predict()


@learning.route('/model_update', methods=['GET', 'POST'])
@flask_login.login_required
def model_update():
    if request.method == 'GET':
        return render_template('model_update.html')
    else:
        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        knowhow = request.form['knowhow']
        yibao = request.form['yibao']
        hospital_level = request.form['hospital_level']
        experience = request.form['experience']
        jinshi = request.form['jinshi']
        incoming = request.form['incoming']
        drink_smoke = request.form['drink_smoke']
        decision = request.form['decision']

@learning.route('/prediction', methods=['GET', 'POST'])
@flask_login.login_required
def prediction():
    if request.method == 'GET':
        return render_template('/prediction.html')
    else:
        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        knowhow = request.form['knowhow']
        yibao = request.form['yibao']
        hospital_level = request.form['hospital_level']
        experience = request.form['experience']
        jinshi = request.form['jinshi']
        incoming = request.form['incoming']
        drink_smoke = request.form['drink_smoke']

        # v_l = [50, '男', '本科', '高', '有', '三甲', '有', '否', 1, '否']
        data = [int(age), gender, education, knowhow, yibao, hospital_level, experience, jinshi, incoming, drink_smoke]
        result = predict.pred_func(data)
        value = Decimal(result[1][0][1] * 100).quantize(Decimal('0.0'))
        return render_template('/prediction_result.html', result=value)


@learning.route('/index', methods=['GET'])
@flask_login.login_required
def index():
    ''' Redirect user the index page, index page can let the user decide whether it's going to input more data or do the prediction.'''
    return render_template('index.html')
