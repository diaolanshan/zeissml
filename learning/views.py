import flask_login
from flask import request, render_template
from . import learning
from learning.model_pred import PredictFactory
from decimal import *
from services.update_model_excel import update_model_excel
from learning.main import train_model
import threading

factory = PredictFactory()


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

        new_row = (
        age, gender, education, knowhow, yibao, hospital_level, experience, jinshi, incoming, drink_smoke, decision)

        new_rows = [new_row for i in range(1)]

        update_model_excel(new_rows)

        threading.Thread(target=dirty_tasks, args=()).start()

    return render_template('/index.html')


def dirty_tasks():
    train_model()

    factory.update_predict()


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
        result = factory.get_predict().pred_func(data)
        value = Decimal(result[1][0][1] * 100).quantize(Decimal('0.0'))
        return render_template('/prediction_result.html', result=value)


@learning.route('/index', methods=['GET'])
@flask_login.login_required
def index():
    ''' Redirect user the index page, index page can let the user decide whether it's going to input more data or do the prediction.'''
    return render_template('index.html')
