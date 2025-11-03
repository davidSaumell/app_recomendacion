from users import User
from usersDAO import usersDAO
import connection as db
from requestHandler import RequestHandler
from flask import Flask, jsonify, request as req

app = Flask(__name__)

if db.connection is None:
    db.init_connection()

@app.route("/recommend/", methods = ["POST"])
def recommend():
    data = req.form.to_dict()
    df = RequestHandler.get_recommendation(data)
    return jsonify(df.to_dict(orient="records"))

@app.route("/train/", methods = ["PATCH"])
def train():
    return RequestHandler.train_model()

@app.route("/version/", methods = ["GET"])
def version():
    return RequestHandler.get_model_version()

@app.route("/test/", methods = ["GET"])
def test():
    data = {"11061": "10", "2476": "1"}
    return RequestHandler.get_recommendation(data)

@app.route("/list-anime/", methods = ["GET"])
def list_anime():
    return jsonify(RequestHandler.get_random_animes())

@app.route("/login/", methods = ["POST"])
def login():
    data = req.form.to_dict()
    username = data[0]
    password = data[1]
    user = User(username, password)
    return jsonify(usersDAO.read_user(user))

@app.route("/signup/", methods = ["POST"])
def signup():
    data = req.form.to_dict()
    username = data[0]
    password = data[1]
    user = User(username, password)
    return jsonify(usersDAO.create_user(user))