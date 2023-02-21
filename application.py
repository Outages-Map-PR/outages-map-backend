from flask import Flask, request, make_response
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
    res = make_response(api)
    return res

@application.route('/hello', methods=['GET'])
def hello_world():
    res = make_response(jsonify({"res" : "Hello World"}))
    return res

if __name__ == '__main__':
    application.run()