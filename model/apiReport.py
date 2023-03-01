from config.dbconfig import pg_config
import psycopg2

class ApiReportDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
        pg_config['user'], pg_config['password'],pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
        
    def getAllApiReports(self):
        cursor = self.conn.cursor()
        query = "select report_id, api_name, report_address, report_type, report_company, report_date from api_report;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAllApiReportsById(self, report_id):
        cursor = self.conn.cursor()
        query = "select report_id, api_name, report_address, report_type, report_company, report_date from api_report where report_id = %s;"
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        return result
    
    def updateApiReport(self, report_id, api_name, report_address, report_type, report_company, report_date):
        cursor = self.conn.cursor()
        query = "update api_report set api_name=%s, report_address=%s, report_type=%s, report_company=%s, report_date=%s where report_id=%s;"
        cursor.execute(query, (api_name, report_address, report_type, report_company, report_date, report_id))
        self.conn.commit()
        return True

    def insertApiReport(self, api_name, report_address, report_type, report_company, report_date):
        cursor = self.conn.cursor()
        query = "insert into api_report (api_name, report_address, report_type, report_company, report_date) values (%s, %s, %s, %s, %s) returning report_id;"
        cursor.execute(query, (api_name, report_address, report_type, report_company, report_date,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id
    
    def deleteApiReport(self, report_id):
        cursor = self.conn.cursor()
        query = "delete from api_report where report_id=%s"
        cursor.execute(query, (report_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0