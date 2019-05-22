import flask_login
from flask import Flask, render_template, redirect, url_for, flash
from flask import request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from learning import learning as zeisslearning

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'oiwihjmcwe02f2'
app.register_blueprint(zeisslearning, url_prefix='/learning')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:106.14.187.169@106.14.187.169:3306/zeissml'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zeissml.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 20
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from models.models import Users
    return Users.query.get(user_id)


login_manager.login_view = '/'
login_manager.login_message = 'Please Login!'
login_manager.session_protection = 'strong'


@app.route('/', methods=['GET'])
def pre_login():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        next_url = request.args.get("next")
        from models.models import Users
        user = Users.query.filter_by(username=username).first()

        if user is not None and user.password == password.strip():
            # set login user
            flask_login.login_user(user)
            return redirect(next_url or url_for('learning.prediction'))
        else:
            flash('用户名或者密码错误')
            return render_template('login.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    # remove the username from the session if it's there
    flask_login.logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
