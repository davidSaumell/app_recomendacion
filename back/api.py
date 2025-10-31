from requestHandler import RequestHandler
from flask import Flask, jsonify, request as req

app = Flask(__name__)

@app.route("/recommend/", methods = ["GET"])
def recommend():
    data = req.form.to_dict()
    return RequestHandler.recommend(data)

@app.route("/train/", methods = ["PATCH"])
def train():
    return RequestHandler.train()

@app.route("/version/", methods = ["GET"])
def version():
    return RequestHandler.version()

@app.route("/test/", methods = ["GET"])
def test():
    data = {"11061": "10", "2476": "1"}
    return RequestHandler.recommend(data)