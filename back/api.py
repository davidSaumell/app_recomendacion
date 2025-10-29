from requestHandler import RequestHandler

@app.route("/recommend", methods = ["GET"])
def recommend():
    return RequestHandler.recommend

@app.route("/train", methods = ["GET"])
def train():
    return RequestHandler.train

@app.route("/version")
def version():
    return RequestHandler.version

@app.route("/test")
def test():
    return RequestHandler.test