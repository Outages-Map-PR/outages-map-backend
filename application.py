# APPLICATION LIBRARIES
from flask import Flask, request, render_template_string
from flask.json import jsonify
import folium
from flask_cors import CORS

# CONTROLLERS
from controllers.user import User
from controllers.outagesMap import OutagesMap
from controllers.apiReport import ApiReport
from controllers.mediaReport import MediaReport
from controllers.user_report import UserReport
from controllers.utilMethods import utilMethods

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(application)


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


@application.route('/API/user/#/<int:user_id>', methods=['GET'])
def userid_routes(user_id):
    if request.method == 'GET':
        res = User().getUserbyID(user_id)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/user/login', methods=['POST'])
def login_route():
    if request.method == 'POST':
        res = User().login(request.json)

        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


# USER REPORT ROUTES
@application.route('/API/report/user', methods=['GET', 'PUT', 'POST'])
def user_report_routes():
    if request.method == 'GET':
        res = UserReport().getAllReports()
        return res
    elif request.method == 'PUT':
        res = UserReport().updateValidation(request.json)
        return res
    elif request.method == 'POST':
        res = UserReport().createReport(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/report/user/match/type', methods=['GET'])
def user_match_type():
    if request.method == 'GET':
        res = UserReport().getSameTypeReports(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/report/user/match/user', methods=['GET'])
def user_match_user():
    if request.method == 'GET':
        res = UserReport().getSameUserReports(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/report/user/match/date', methods=['GET'])
def user_match_date():
    if request.method == 'GET':
        res = UserReport().getSameDateReports(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/report/user/match/address', methods=['GET'])
def user_match_address():
    if request.method == 'GET':
        res = UserReport().getSameAddressReports(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


@application.route('/API/report/user/match/company', methods=['GET'])
def user_match_company():
    if request.method == 'GET':
        res = UserReport().getSameCompanyReports(request.json)
        return res
    else:
        res = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return jsonify(res)


# OUTAGES MAP REPORT ROUTES

@application.route('/API/outagesmap', methods=['GET', 'POST', 'PUT'])
def outagesmap_route():
    if request.method == 'GET':
        res = OutagesMap().getAllOutages()
        return res
    elif request.method == 'POST':
        res = OutagesMap().insertOutages(request.json)
        return res
    elif request.method == 'PUT':
        res = OutagesMap().updateOutages(request.json)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/outagesmap/<int:outages_id>', methods=['GET', 'DELETE'])
def outagesmap_byid_route(outages_id):
    if request.method == 'GET':
        res = OutagesMap().getOutagesById(outages_id)
        return res
    elif request.method == 'DELETE':
        res = OutagesMap().deleteOutages(outages_id)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/outagesmap/reportid/<int:report_id>', methods=['GET', 'DELETE'])
def outages_map_byreportid_route(report_id):
    if request.method == 'GET':
        res = OutagesMap().getOutagesByReportId(report_id)
        return res
    elif request.method == 'DELETE':
        res = OutagesMap().deleteOutagesByReportId(report_id)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


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


@application.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        location=[18.2269, -66.391],
        width=800,
        height=600,
        zoom_start=9
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )

# UTILITY METHODS ROUTES

@application.route('/API/utils/latlon', methods=['GET'])
def address_to_latlon():
    if request.method == 'GET':
        res = utilMethods().addressToLatLong(request.json)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err

if __name__ == '__main__':
    application.run()
