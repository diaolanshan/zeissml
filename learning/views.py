import flask_login
from flask import request, render_template
from . import learning


@learning.route('/model_update', methods=['GET', 'POST'])
@flask_login.login_required
def model_update():
    if request.method == 'GET':
        return render_template('model_update.html')
    else:
        age = request.form['age']
        gender = request.form['gender']


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

        result = 82

        return render_template('/prediction_result.html', result = result)


@learning.route('/index', methods=['GET'])
@flask_login.login_required
def index():
    ''' Redirect user the index page, index page can let the user decide whether it's going to input more data or do the prediction.'''
    return render_template('index.html')
