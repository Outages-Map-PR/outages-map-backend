from flask import jsonify
from model.outagesMap import OutagesMapDAO

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
        return jsonify(result)
    
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
        