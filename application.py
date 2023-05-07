# APPLICATION LIBRARIES
from flask import Flask, request, render_template_string
from flask.json import jsonify
import folium
import threading
import time
from flask_cors import CORS
from collections import defaultdict

# CONTROLLERS
from controllers.user import User
from controllers.outagesMap import OutagesMap
from controllers.apiReport import ApiReport
from controllers.mediaReport import MediaReport
from controllers.user_report import UserReport
from controllers.utilMethods import utilMethods
from controllers.analytics import serviceAnalytics

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


@application.route('/API/user/<int:user_id>', methods=['GET', 'OPTIONS'])
def userid_routes(user_id):
    if request.method == 'GET':
        res = User().getUserbyID(user_id)
        # res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    elif request.method == 'OPTIONS':
        res = OutagesMap().insertUserOutages(user_id)
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
@application.route('/API/userreport', methods=['GET', 'PUT', 'POST'])
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


@application.route('/API/report/<user_email>', methods=['GET'])
def user_match_user(user_email):
    if request.method == 'GET':
        res = UserReport().getSameUserReports(str(user_email))
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

@application.route('/API/outagesmap', methods=['GET', 'POST', 'PUT', 'OPTIONS', 'PATCH'])
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
    elif request.method == 'OPTIONS':
        res = OutagesMap().getLastTenOutages()
        return res
    elif request.method == 'PATCH':
        res = OutagesMap().getHistoricalOutages()
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


@application.route('/API/mediareport/<int:report_id>', methods=['GET', 'DELETE', 'OPTIONS'])
def mediareport_byid_route(report_id):
    if request.method == 'GET':
        res = MediaReport().getMediaReportById(report_id)
        return res
    elif request.method == 'DELETE':
        res = MediaReport().deleteMediaReport(report_id)
        return res
    elif request.method == 'OPTIONS':
        res = OutagesMap().insertMediaOutages(report_id)
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


@application.route('/API/apireport/<int:report_id>', methods=['GET', 'DELETE', 'OPTIONS'])
def apireport_byid_route(report_id):
    if request.method == 'GET':
        res = ApiReport().getApiReportById(report_id)
        return res
    elif request.method == 'DELETE':
        res = ApiReport().deleteApiReport(report_id)
        return res
    elif request.method == 'OPTIONS':
        res = OutagesMap().insertAPIOutages(report_id)
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route("/map/<string:page>")
def home_map(page):
    """Extract map components and put those on a page."""
    m = folium.Map(
        location=[18.2269, -66.391],
        zoom_start=9
    )

    filters = request.args['filters']

    if page == 'home':

        function_data = latlongsFilterByType(filters)

        water = function_data[0]
        power = function_data[1]
        internet = function_data[2]

        if len(water) != 0:
            for i in range(0, len(water['lat'])):
                folium.Marker(
                    location=[water['lat'][i], water['lng'][i]],
                    popup=water['type'][i],
                    icon=folium.Icon(icon_color='black', icon='fa-tint', prefix='fa', color='lightblue')
                ).add_to(m)

        if len(power) != 0:
            for i in range(0, len(power['lat'])):
                folium.Marker(
                    location=[power['lat'][i], power['lng'][i]],
                    popup=power['type'][i],
                    icon=folium.Icon(icon_color='black', icon='fa-plug', prefix='fa', color='blue')
                ).add_to(m)

        if len(internet) != 0:
            for i in range(0, len(internet['lat'])):
                folium.Marker(
                    location=[internet['lat'][i], internet['lng'][i]],
                    popup=internet['type'][i],
                    icon=folium.Icon(icon_color='black', icon='fa-laptop', prefix='fa', color='darkblue')
                ).add_to(m)

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

@application.route('/API/utils/latlon', methods=['GET', 'OPTIONS'])
def address_to_latlon():
    if request.method == 'GET':
        res = utilMethods().addressToLatLong(request.json)
        return res
    elif request.method == 'OPTIONS':
        res = latlongsFilterByType(["all"])
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/analytics/all', methods=['GET'])
def get_all_analytics():
    try:
        request.args['date']
    except:
        return jsonify({"error": "NO 'date' FIELD SPECIFIED"})
    if request.method == 'GET':
        res = serviceAnalytics().getAllAnalytics(request.args['date'])
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/analytics/power', methods=['GET'])
def get_power_analytics():
    try:
        request.args['date']
    except:
        return jsonify({"error": "NO 'date' PARAM SPECIFIED"})
    if request.method == 'GET':
        res = serviceAnalytics().getServiceAnalytics(request.args['date'], 'power')
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/analytics/water', methods=['GET'])
def get_water_analytics():
    try:
        request.args['date']
    except:
        return jsonify({"error": "NO 'date' PARAM SPECIFIED"})
    if request.method == 'GET':
        res = serviceAnalytics().getServiceAnalytics(request.args['date'], 'water')
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/analytics/internet', methods=['GET'])
def get_internet_analytics():
    try:
        request.args['date']
    except:
        return jsonify({"error": "NO 'date' PARAM SPECIFIED"})
    if request.method == 'GET':
        res = serviceAnalytics().getServiceAnalytics(request.args['date'], 'internet')
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


@application.route('/API/analytics/count', methods=['GET'])
def get_analytics_count():
    try:
        request.args['date']
    except:
        return jsonify({"error": "NO 'date' PARAM SPECIFIED"})
    if request.method == 'GET':
        res = serviceAnalytics().getAllAnalyticsAndCount(request.args['date'])
        return res
    else:
        err = {"error": "METHOD NOT SUPPORTED IN ROUTE"}
        return err


# HELPER FUNCTIONS FOR MAP
def latlongsFilterByType(filters):
    res = OutagesMap().getAllOutages()
    water = defaultdict(list)
    power = defaultdict(list)
    internet = defaultdict(list)

    result = []

    for outages in res:
        dict_outage = dict(outages)
        if dict_outage['active'] == False:
            continue
        type_outage = dict_outage['outage_type']
        if type_outage == 'water':
            water['lat'].append(dict_outage['outage_lat'])
            water['lng'].append(dict_outage['outage_lng'])
            water['type'].append(dict_outage['outage_type'])
        if type_outage == 'power':
            power['lat'].append(dict_outage['outage_lat'])
            power['lng'].append(dict_outage['outage_lng'])
            power['type'].append(dict_outage['outage_type'])
        if type_outage == 'internet':
            if (dict_outage['outage_company'] == 'Liberty' and 'liberty' in filters) or \
                    (dict_outage['outage_company'] == 'Claro' and 'claro' in filters) or \
                    (dict_outage['outage_company'] == 'AT&T' and 'at&t' in filters) or \
                    'all' in filters:
                internet['lat'].append(dict_outage['outage_lat'])
                internet['lng'].append(dict_outage['outage_lng'])
                internet['type'].append(dict_outage['outage_type'])

    if "water" in filters or "all" in filters:
        result.append(water)
    else:
        result.append([])
    if "power" in filters or "all" in filters:
        result.append(power)
    else:
        result.append([])
    if "internet" in filters or "all" in filters:
        result.append(internet)
    else:
        result.append([])

    return result

def thread_monitor_outages():
    while True:
        print(utilMethods().monitor_outages())
        time.sleep(3600)

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=thread_monitor_outages)
    monitor_thread.start()
    application.run()
