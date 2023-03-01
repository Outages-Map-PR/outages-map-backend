# APPLICATION LIBRARIES
from flask import Flask, request
from flask.json import jsonify

# CONTROLLERS
from controllers.user import User
from controllers.mediaReport import MediaReport

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

# MEDIA REPORT ROUTES
@application.route('/API/mediareport', methods=['GET', 'POST', 'PUT'])
def mediareport_route():
    if request.method == 'GET':
        res = MediaReport().getAllMediaReports()
        return res
    elif request.method == 'POST':
        res = MediaReport().insertMediaReport(request.json)
        return res
    elif request.method == 'PUT':
        res = MediaReport().updateMediaReport(request.json)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err
    
@application.route('/API/mediareport/<int:report_id>', methods=['GET', 'DELETE'])
def mediareport_byid_route(report_id):
    if request.method == 'GET':
        res = MediaReport().getMediaReportById(report_id)
        return res
    elif request.method == 'DELETE':
        res = MediaReport().deleteMediaReport(report_id)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err

if __name__ == '__main__':
    application.run()