from requestHandler import RequestHandler
from flask import Flask, jsonify, request as req

app = Flask(__name__)

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
    return RequestHandler.get_recommendation(data)

@app.route("/list-anime/", methods = ["GET"])
def list_anime():
    return jsonify(RequestHandler.get_random_animes())