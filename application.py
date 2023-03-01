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
        "/": "Current view",
        "/hello": "Example view of hello world",
        "/API": {
            "/user": "USER API ROUTE"
        }
    }
    res = jsonify(api)
    return res


@application.route('/hello', methods=['GET'])
def hello_world():
    res = jsonify({"res": "Hello World"})
    return res


# USER API ROUTES
@application.route('/API/user', methods=['GET', 'PUT', 'POST', 'DELETE'])
def user_route():
    if request.method == 'GET':
        res = User().getAllUsers()
        return res
    elif request.method == 'PUT':
        res = User().updateUser(request.json)
        return res
    elif request.method == 'POST':
        res = User().insertUser(request.json)
        return res
    elif request.method == 'DELETE':
        res = User().deleteUser(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/user/login', methods=['GET'])
def login_route():
    if request == 'GET':
        res = User().login(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


if __name__ == '__main__':
    application.run()
