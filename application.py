# APPLICATION LIBRARIES
from flask import Flask, request, make_response
from flask.json import jsonify
# from flask_cors import CORS, cross_origin

# CONTROLLERS
from controllers.user import User

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# CORS(application, resources={
#     r"/*": {"origins": "*"}
# }, supports_credentials=True)

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
        # res = make_response(User().getAllUsers())
        # res.headers['Access-Control-Allow-Origin'] = '*'
        # return res
        return User().getAllUsers()
    else:
        # res = make_response({"error": "METHOD NOT SUPPORTED IN ROUTE"})
        # res.headers['Access-Control-Allow-Origin'] = '*'
        # return res
        return {"error": "METHOD NOT SUPPORTED IN ROUTE"}

if __name__ == '__main__':
    application.run()