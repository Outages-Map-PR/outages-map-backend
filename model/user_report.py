from config.dbconfig import pg_config
import psycopg2


class UserReportDao:
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
                                                                            pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllReports(self):
        cursor = self.conn.cursor()
        query = "select report_id, user_name, report_address, report_type, report_company, report_date, report_validated from \"user_report\""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getSameTypeReports(self, report_type):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where report_type = %s"
        cursor.execute(query, report_type)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getSameUserReports(self, user_name):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where user_email = %s"
        cursor.execute(query, user_name)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getSameDateReports(self, date):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where report_date = %s"
        cursor.execute(query, date)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getSameAddressReports(self, address):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where report_address = %s"
        cursor.execute(query, address)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def getSameCompanyReports(self, company):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where report_company = %s"
        cursor.execute(query, company)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def createReport(self, user_name, report_address, report_type, report_company):
        cursor = self.conn.cursor()
        query = "insert into \"user_report\" (user_name, report_address, report_type, report_company, report_date, " \
                "report_validated) values (%s, %s, %s, %s, current_date, false) returning report_id"
        cursor.execute(query, (user_name, report_address, report_type, report_company))
        report_id = cursor.fetchone()[0]
        self.conn.commit()
        return report_id

    def getAllUserReportsById(self, report_id):
        cursor = self.conn.cursor()
        query = "select report_id, user_name, report_address, report_type, report_company, report_date from \"user_report\" where report_id = %s;"
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        return result

    def updateValidation(self, report_id):
        cursor = self.conn.cursor()
        query = "update \"user_report\" set report_validated = true where report_id = %s"
        cursor.execute(query, report_id)
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0

    def validatedReports(self):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where report_validated"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def notValidatedReports(self):
        cursor = self.conn.cursor()
        query = "select user_name, report_address, report_date from \"user_report\" where not report_validated"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result
