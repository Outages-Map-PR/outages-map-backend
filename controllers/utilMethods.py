from flask import jsonify
from model.utilMethods import utilMethodsDAO

class utilMethods:
    
    def addressToLatLong(self, address):
        if (address['address']):
            pos = utilMethodsDAO().addressToLatLon(address)
            if isinstance(pos, tuple):
                res = {
                    "Latitude": pos[0],
                    "Longitude": pos[1]
                }
                return jsonify(res)
            else: 
                return jsonify({"error": "ADDRESS NOT FOUND, MAY NEED A MORE GENERAL ADDRESS"})
        else:
            return jsonify({"error": "NO 'address' SPECIFIED IN REQUEST"})