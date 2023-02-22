# APPLICATION LIBRARIES
from flask import Flask, request
from flask.json import jsonify

# CONTROLLERS
from controllers.user import User

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@application.route('/', methods=['GET'])
def home():
    api = {
        "/" : "Current view",
        "/hello" : "Example view of hello world",
        "/API" : {
            "/user" : "USER API ROUTE"
        }
    }
    res = jsonify(api)
    return res

@application.route('/hello', methods=['GET'])
def hello_world():
    res = jsonify({"res" : "Hello World"})
    return res

# USER API ROUTES
@application.route('/API/user', methods=['GET'])
def user_route():
    if request.method == 'GET':
        res = User().getAllUsers()
        return res
    else:
        return {"error": "METHOD NOT SUPPORTED IN ROUTE"}

if __name__ == '__main__':
    application.run()