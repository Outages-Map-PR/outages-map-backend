from flask import Flask, request
from flask.json import jsonify

application = Flask(__name__)

@application.route('/', methods=['GET'])
def home():
    api = {
        "/" : "Current view",
        "/hello" : "Example view of hello world",
        "/API" : {
            "/users" : ""
        }
    }
    res = jsonify(api)
    return res

@application.route('/hello', methods=['GET'])
def hello_world():
    res = jsonify({"res" : "Hello World"})
    return res

if __name__ == '__main__':
    application.run()