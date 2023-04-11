from flask import jsonify
from controllers.outagesMap import OutagesMap
from model.analytics import analyticsDAO

# Definitions
POWER = 'power'
WATER = 'water'
INTERNET = 'internet'

class serviceAnalytics:
        
    def getServiceAnalytics(self, date, type):
        tuples = []
        result = []
        if type == POWER:
            tuples = analyticsDAO().getServiceAnalytics(date, POWER)
        elif type == WATER:
            tuples = analyticsDAO().getServiceAnalytics(date, WATER) 
        elif type == INTERNET:
            tuples = analyticsDAO().getServiceAnalytics(date, INTERNET) 
        om = OutagesMap()
        for t in tuples:
            result.append(om.build_row_dict(t))
        return jsonify(result)
    
    def getAllAnalytics(self, date):
        om = OutagesMap()
        result = {
            POWER: [],
            WATER: [],
            INTERNET: []
        }
        t_list = analyticsDAO().getAllAnalytics(date)
        for t in t_list[0]:
            result[POWER].append(om.build_row_dict(t))
        for t in t_list[1]:
            result[WATER].append(om.build_row_dict(t))
        for t in t_list[2]:
            result[INTERNET].append(om.build_row_dict(t))
        return jsonify(result)