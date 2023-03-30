from flask import jsonify

from controllers.outagesMap import OutagesMap
from model.apiReport import ApiReportDAO

class ApiReport:
    
    def build_row_dict(self, row):
        if row:
            result = {
                "report_id": row[0],
                "api_name": row[1],
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
    
    def build_attr_dict(self, report_id, api_name, report_address, report_type, report_company, report_date):
        result = {
            "report_id": report_id,
            "api_name": api_name,
            "report_address": report_address,
            "report_type": report_type,
            "report_company": report_company,
            "report_date": report_date
        }
        return result
    
    def getAllApiReports(self):
        dao = ApiReportDAO()
        tuples = dao.getAllApiReports()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)
    
    def getApiReportById(self, report_id):
        dao = ApiReportDAO()
        t = dao.getAllApiReportsById(report_id)
        result = self.build_row_dict(t)
        return jsonify(result)
    
    def updateApiReport(self, json):
        report_id = json['report_id']
        api_name = json['api_name']
        report_address = json['report_address']
        report_type = json['report_type']
        report_company = json['report_company']
        report_date = json['report_date']
        dao = ApiReportDAO()
        update_status = dao.updateApiReport(report_id, api_name, report_address, report_type, report_company, report_date)
        result = self.build_attr_dict(report_id, api_name, report_address, report_type, report_company, report_date)
        return jsonify(result)
    
    def insertApiReport(self, json):
        api_name = json['api_name']
        report_address = json['report_address']
        report_type = json['report_type']
        report_company = json['report_company']
        dao = ApiReportDAO()
        report_id = dao.insertApiReport(api_name, report_address, report_type, report_company)
        result = self.build_attr_dict(report_id, api_name, report_address, report_type, report_company, "today")
        outage_insert = OutagesMap().insertAPIOutages(report_id)
        return outage_insert
        
    def deleteApiReport(self, report_id):
        dao = ApiReportDAO()
        result = dao.deleteApiReport(report_id)
        if result:
            return jsonify(result)
        else:
            return jsonify("REPORT NOT FOUND")