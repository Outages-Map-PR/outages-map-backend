# APPLICATION LIBRARIES
from flask import Flask, request
from flask.json import jsonify

# CONTROLLERS
from controllers.user import User
from controllers.apiReport import ApiReport

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
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return res

# API REPORT ROUTES
@application.route('/API/apireport', methods=['GET', 'POST', 'PUT'])
def apireport_route():
    if request.method == 'GET':
        res = ApiReport().getAllApiReports()
        return res
    elif request.method == 'POST':
        res = ApiReport().insertApiReport(request.json)
        return res
    elif request.method == 'PUT':
        res = ApiReport().updateApiReport(request.json)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err
    
@application.route('/API/apireport/<int:report_id>', methods=['GET', 'DELETE'])
def apireport_byid_route(report_id):
    if request.method == 'GET':
        res = ApiReport().getApiReportById(report_id)
        return res
    elif request.method == 'DELETE':
        res = ApiReport().deleteApiReport(report_id)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err

if __name__ == '__main__':
    application.run()