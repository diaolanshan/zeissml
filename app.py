from flask import Flask, render_template, redirect, url_for, make_response, abort, flash, session
from flask import request
import flask_login
from flask_login import LoginManager, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'oiwihjmcwe02f2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@szhpc6287:3306/zeissml'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from zeiss_models import Users
    return Users.query.get(user_id)

login_manager.login_view = '/'
login_manager.login_message = 'Please Login!'
login_manager.session_protection = 'strong'


@app.route('/', methods=['GET'])
def pre_login():
    return render_template("login.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        next_url = request.args.get("next")
        from zeiss_models import Users
        user = Users.query.filter_by(username=username).first()

        if user is not None and user.password == password.strip():
            #set login user
            flask_login.login_user(user)
            return redirect(next_url or url_for('index'))
        else:
            flash('用户名或者密码错误')

    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
@flask_login.login_required
def index():
    return render_template('index.html')

@app.route('/model_update', methods=['POST'])
@flask_login.login_required
def model_update():
    age = request.form['age']
    gender = request.form['gender']

@app.route('/logout')
@flask_login.login_required
def logout():
    # remove the username from the session if it's there
    flask_login.logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
