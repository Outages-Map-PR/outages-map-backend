from flask import jsonify

from controllers.outagesMap import OutagesMap
from model.user_report import UserReportDao


class UserReport:
    def build_row_dic(self, row):
        result = {
            "report_id": row[0],
            "user_name": row[1],
            "report_address": row[2],
            "report_type": row[3],
            "report_company": row[4],
            "report_date": row[5],
            "report_validated": row[6]
        }
        return result

    def build_attr_dic(self, report_id, user_name, report_address, report_type, report_company, report_date,
                       report_validated):
        result = {'report_id': report_id, 'user_name': user_name, 'report_address': report_address,
                  'report_type': report_type, 'report_company': report_company, 'report_date': report_date,
                  'report_validated': report_validated}
        return result

    def getAllReports(self):
        dao = UserReportDao()
        reports = dao.getAllReports()
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def getApiReportById(self, report_id):
        dao = UserReportDao()
        t = dao.getAllUserReportsById(report_id)
        result = self.build_row_dict(t)
        return jsonify(result)

    def getSameTypeReports(self, json):
        dao = UserReportDao()
        reports = dao.getSameTypeReports(json[0])
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def getSameUserReports(self, json):
        dao = UserReportDao()
        reports = dao.getSameUserReports(json[0])
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def getSameDateReports(self, json):
        dao = UserReportDao()
        reports = dao.getSameDateReports(json[0])
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def getSameAddressReports(self, json):
        dao = UserReportDao()
        reports = dao.getSameAddressReports(json[0])
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def getSameCompanyReports(self, json):
        dao = UserReportDao()
        reports = dao.getSameCompanyReports(json[0])
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def createReport(self, json):
        dao = UserReportDao()
        user_name = json["user_name"]
        report_address = json["report_address"]
        report_type = json["report_type"]
        report_company = json["report_company"]
        report_id = dao.createReport(user_name, report_address, report_type, report_company)
        outage_map = OutagesMap().insertUserOutages(report_id)
        if report_id:
            return outage_map
        else:
            return jsonify("REPORT NOT ADDED")

    def updateValidation(self, json):
        dao = UserReportDao()
        rows_changed = dao.updateValidation()
        if rows_changed:
            return jsonify("REPORT UPDATED"), 200
        else:
            return jsonify("REPORT NOT FOUND"), 400

    def validatedReport(self):
        dao = UserReportDao()
        reports = dao.validatedReports()
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404

    def notValidatedReport(self):
        dao = UserReportDao()
        reports = dao.notValidatedReports()
        result = []
        for report in reports:
            result.append(self.build_row_dic(report))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("REPORTS NOT FOUND"), 404
