from requestHandler import RequestHandler
from flask import Flask, jsonify, request as req

app = Flask(__name__)

@app.route("/recommend", methods = ["GET"])
def recommend():
    data = req.get_json()
    return RequestHandler.recommend(data)

@app.route("/train", methods = ["PATCH"])
def train():
    return RequestHandler.train

@app.route("/version", methods = ["GET"])
def version():
    return RequestHandler.version

@app.route("/test", methods = ["GET"])
def test():
    return RequestHandler.test