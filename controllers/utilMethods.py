from flask import jsonify
from model.utilMethods import utilMethodsDAO

class utilMethods:
    
    def addressToLatLong(self, req):
        try:
            res = utilMethodsDAO().addressToLatLon(req['address'])
            return jsonify(res)
        except:
            return jsonify({"error": "NO 'address' SPECIFIED IN REQUEST"})
            