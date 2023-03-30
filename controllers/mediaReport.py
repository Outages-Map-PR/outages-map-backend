from flask import jsonify

from controllers.outagesMap import OutagesMap
from model.mediaReport import MediaReportDAO

class MediaReport:
    
    def build_row_dict(self, row):
        if row:
            result = {
                "report_id": row[0],
                "media_type": row[1],
                "report_address": row[2], 
                "report_type": row[3],
                "report_company": row[4],
                "report_date": row[5]
            }
        else:
            result = {
                "error": "404",
                "message": "REPORT NOT FOUND"
            }
        return result
    
    def build_attr_dict(self, report_id, media_type, report_address, report_type, report_company, report_date):
        result = {
            "report_id": report_id,
            "media_type": media_type,
            "report_address": report_address,
            "report_type": report_type,
            "report_company": report_company,
            "report_date": report_date
        }
        return result
    
    def getAllMediaReports(self):
        dao = MediaReportDAO()
        tuples = dao.getAllMediaReports()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)
    
    def getMediaReportById(self, report_id):
        dao = MediaReportDAO()
        t = dao.getAllMediaReportsById(report_id)
        result = self.build_row_dict(t)
        return jsonify(result)
    
    def updateMediaReport(self, json):
        report_id = json['report_id']
        media_type = json['media_type']
        report_address = json['report_address']
        report_type = json['report_type']
        report_company = json['report_company']
        report_date = json['report_date']
        dao = MediaReportDAO()
        update_status = dao.updateMediaReport(report_id, media_type, report_address, report_type, report_company, report_date)
        result = self.build_attr_dict(report_id, media_type, report_address, report_type, report_company, report_date)
        return jsonify(result)
    
    def insertMediaReport(self, json):
        media_type = json['media_type']
        report_address = json['report_address']
        report_type = json['report_type']
        report_company = json['report_company']
        dao = MediaReportDAO()
        report_id = dao.insertMediaReport(media_type, report_address, report_type, report_company)
        result = self.build_attr_dict(report_id, media_type, report_address, report_type, report_company, "today")
        outage_map = OutagesMap().insertMediaOutages(report_id)
        return outage_map
        
    def deleteMediaReport(self, report_id):
        dao = MediaReportDAO()
        result = dao.deleteMediaReport(report_id)
        if result:
            return jsonify(result)
        else:
            return jsonify("REPORT NOT FOUND")