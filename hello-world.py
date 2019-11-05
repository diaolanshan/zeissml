from flask import Flask, jsonify, request
from flask_cors import cross_origin
import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object(__name__)

auth = HTTPBasicAuth()

users = {
    "talhongkong": generate_password_hash("talhongkong")
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route("/po", methods=["GET", "POST"])
@auth.login_required
def receive_po():
    if request.method == 'GET':
        return jsonify({"Error":"Method not supported, please use POST."})

    po_file = request.get_json(force=True)

    print(po_file)

    return "Hello, %s!" % auth.username()


@app.route("/")
@cross_origin()
@auth.login_required
def endpoint():
    t = {}
    # t['data'] =
    return jsonify({'data': [{"id": 1, "name": "Java"}, {"id": 2, "name": "Python"}]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
