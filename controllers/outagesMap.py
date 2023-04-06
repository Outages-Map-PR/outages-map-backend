from flask import jsonify

from controllers.utilMethods import utilMethods
from model.apiReport import ApiReportDAO
from model.mediaReport import MediaReportDAO
from model.outagesMap import OutagesMapDAO
from model.user_report import UserReportDao
from model.utilMethods import utilMethodsDAO


class OutagesMap:
    
    def build_row_dict(self, row):
        if row:
            result = {
                "outages_id": row[0],
                "report_id": row[1],
                "outage_type": row[2], 
                "outage_lat": row[3],
                "outage_lng": row[4],
                "outage_source": row[5],
                "outage_date": row[6],
                "outage_company": row[7],
                "active": row[8]
            }
        else:
            result = {
                "error": "404",
                "message": "OUTAGE MAP REPORT NOT FOUND"
            }
        return result
    
    def build_attr_dict(self, outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active):
        result = {
            "outages_id": outages_id,
            "report_id": report_id,
            "outage_type": outage_type,
            "outage_lat": outage_lat,
            "outage_lng": outage_lng,
            "outage_source": outage_source,
            "outage_date": outage_date,
            "outage_company": outage_company,
            "active": active,
        }
        return result
    
    def getAllOutages(self):
        dao = OutagesMapDAO()
        tuples = dao.getAllOutages()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return result

    def getLastTenOutages(self):
        dao = OutagesMapDAO()
        tuples = dao.getLastTenOutages()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return result

    def getHistoricalOutages(self):
        dao = OutagesMapDAO()
        tuples = dao.getHistoricalOutages()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return result
    
    def getOutagesById(self, outages_id):
        dao = OutagesMapDAO()
        t = dao.getOutagesById(outages_id)
        result = self.build_row_dict(t)
        return jsonify(result)
    
    def getOutagesByReportId(self, report_id):
        dao = OutagesMapDAO()
        t = dao.getOutagesByReportId(report_id)
        result = self.build_row_dict(t)
        return jsonify(result)
            
    def updateOutages(self, json):
        outages_id = json['outages_id']
        report_id = json['report_id']
        outage_type = json['outage_type']
        outage_lat = json['outage_lat']
        outage_lng = json['outage_lng']
        outage_source = json['outage_source']
        outage_date = json['outage_date']
        outage_company = json['outage_company']
        active = json['active']
        dao = OutagesMapDAO()
        update_status = dao.updateOutages(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active)
        result = self.build_attr_dict(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active)
        return jsonify(result)
    
    def insertOutages(self, json):
        report_id = json['report_id']
        outage_type = json['outage_type']
        outage_lat = json['outage_lat']
        outage_lng = json['outage_lng']
        outage_source = json['outage_source']
        outage_date = json['outage_date']
        outage_company = json['outage_company']
        active = json['active']
        dao = OutagesMapDAO()
        outages_id = dao.insertOutages(report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active)
        result = self.build_attr_dict(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active)
        return jsonify(result)

    def insertAPIOutages(self, report_id):
        json = ApiReportDAO().getAllApiReportsById(report_id)
        if not json:
            return jsonify("REPORT NOT FOUND")
        # return str(json[6])
        coordinates = utilMethodsDAO().addressToLatLon(json[2])
        for lat_lng in coordinates:
            if lat_lng != "ERROR":
                arr = coordinates[lat_lng].split(",")
                latitude = arr[0]
                longitude = arr[1]
                break
        report_id = json[0]
        outage_type = json[3]
        outage_lat = latitude
        outage_lng = longitude
        outage_source = "API " + json[1]
        outage_date = json[5]
        outage_company = json[4]
        active = True
        dao = OutagesMapDAO()
        outages_id = dao.insertOutages(report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date,
                                       outage_company, active)
        result = self.build_attr_dict(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source,
                                      outage_date, outage_company, active)
        return jsonify(result)

    def insertMediaOutages(self, report_id):
        json = MediaReportDAO().getAllMediaReportsById(report_id)
        if not json:
            return jsonify("REPORT NOT FOUND")
        # return str(json)
        coordinates = utilMethodsDAO().addressToLatLon(json[2])
        for lat_lng in coordinates:
            if coordinates[lat_lng] != "ERROR":
                arr = coordinates[lat_lng].split(",")
                latitude = arr[0]
                longitude = arr[1]
                break
        report_id = json[0]
        outage_type = json[3]
        outage_lat = latitude
        outage_lng = longitude
        outage_source = "Media " + json[1]
        outage_date = json[5]
        outage_company = json[4]
        active = True
        dao = OutagesMapDAO()
        outages_id = dao.insertOutages(report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date,
                                       outage_company, active)
        result = self.build_attr_dict(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source,
                                      outage_date, outage_company, active)
        return jsonify(result)


    def insertUserOutages(self, report_id):
        json = UserReportDao().getAllUserReportsById(report_id)
        if not json:
            return jsonify("REPORT NOT FOUND")
        # return str(json)
        coordinates = utilMethodsDAO().addressToLatLon(json[2])
        for lat_lng in coordinates:
            if coordinates[lat_lng] != "ERROR":
                arr = coordinates[lat_lng].split(",")
                latitude = arr[0]
                longitude = arr[1]
                break
        report_id = json[0]
        outage_type = json[3]
        outage_lat = latitude
        outage_lng = longitude
        outage_source = "User " + json[1]
        outage_date = json[5]
        outage_company = json[4]
        active = True
        dao = OutagesMapDAO()
        outages_id = dao.insertOutages(report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date,
                                       outage_company, active)
        result = self.build_attr_dict(outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source,
                                      outage_date, outage_company, active)
        return jsonify(result)
        
    def deleteOutages(self, outages_id):
        dao = OutagesMapDAO()
        result = dao.deleteOutages(outages_id)
        if result:
            return jsonify(result)
        else:
            return jsonify("OUTAGES MAP REPORT NOT FOUND")
        
    def deleteOutagesByReportId(self, report_id):
        dao = OutagesMapDAO()
        result = dao.deleteOutagesByReportId(report_id)
        if result:
            return jsonify(result)
        else:
            return jsonify("OUTAGES MAP REPORT NOT FOUND")
        