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
    model_version, artifact_path = RequestHandler.get_model_version()
    
    return jsonify({
        "model_version": model_version,
        "artifact_path": artifact_path
    })

@app.route("/test/", methods = ["GET"])
def test():
    data = {"11061": "10", "2476": "1"}
    df = RequestHandler.get_recommendation(data)
    return jsonify(df.to_dict(orient="records"))

@app.route("/list-anime/", methods = ["GET"])
def list_anime():
    df = RequestHandler.get_random_animes()
    return jsonify(df.to_dict(orient="records"))

@app.route("/login/", methods = ["POST"])
def login():
    data = req.form.to_dict()
    username = data["username"]
    password = data["password"]
    user = User(username, password)
    users = usersDAO.read_user(user)
    users_JSON = []
    for user in users:
        users_JSON.append({
            "userid": user.get_userid(), 
            "username": user.get_username(), 
            "password": user.get_password()
            })

    return jsonify(users_JSON)

@app.route("/signup/", methods = ["POST"])
def signup():
    data = req.form.to_dict()
    username = data["username"]
    password = data["password"]
    user = User(username, password)
    user = usersDAO.create_user(user)
    user_JSON = [{
            "userid": user.get_userid(), 
            "username": user.get_username(), 
            "password": user.get_password()
            }]

    return jsonify(user_JSON)