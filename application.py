from flask import Flask, request, make_response
from flask.json import jsonify

application = Flask(__name__)

@application.route('/hello', methods=['GET'])
def hello_world():
    res = make_response("Hello, World!")
    return res

if __name__ == '__main__':
    application.run()