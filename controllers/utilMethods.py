from flask import jsonify
from model.utilMethods import utilMethodsDAO


class utilMethods:

    def addressToLatLong(self, req):
        try:
            res = utilMethodsDAO().addressToLatLon(req['address'])
            return jsonify(res)
        except:
            return jsonify({"error": "NO 'address' SPECIFIED IN REQUEST"})
        
    def monitor_outages(self):
        res = utilMethodsDAO().monitor_outages()
        return jsonify(f"UPDATED REPORTS: {res}")