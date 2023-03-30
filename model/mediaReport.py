from config.dbconfig import pg_config
import psycopg2

class MediaReportDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
        pg_config['user'], pg_config['password'],pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
        
    def getAllMediaReports(self):
        cursor = self.conn.cursor()
        query = "select report_id, media_type, report_address, report_type, report_company, report_date from media_report;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAllMediaReportsById(self, report_id):
        cursor = self.conn.cursor()
        query = "select report_id, media_type, report_address, report_type, report_company, report_date from media_report where report_id = %s;"
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        return result
    
    def updateMediaReport(self, report_id, media_type, report_address, report_type, report_company, report_date):
        cursor = self.conn.cursor()
        query = "update media_report set media_type=%s, report_address=%s, report_type=%s, report_company=%s, report_date=%s where report_id=%s;"
        cursor.execute(query, (media_type, report_address, report_type, report_company, report_date, report_id))
        self.conn.commit()
        return True

    def insertMediaReport(self, media_type, report_address, report_type, report_company):
        cursor = self.conn.cursor()
        query = "insert into media_report (media_type, report_address, report_type, report_company, report_date) values (%s, %s, %s, %s, current_date) returning report_id;"
        cursor.execute(query, (media_type, report_address, report_type, report_company,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id
    
    def deleteMediaReport(self, report_id):
        cursor = self.conn.cursor()
        query = "delete from media_report where report_id=%s"
        cursor.execute(query, (report_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0