from config.dbconfig import pg_config
import psycopg2

class OutagesMapDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
        pg_config['user'], pg_config['password'],pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
        
    def getAllOutages(self):
        cursor = self.conn.cursor()
        query = "select outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active from outages_map;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getOutagesById(self, outages_id):
        cursor = self.conn.cursor()
        query = "select outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active from outages_map where outages_id = %s;"
        cursor.execute(query, (outages_id,))
        result = cursor.fetchone()
        return result
    
    def getOutagesByReportId(self, report_id):
        cursor = self.conn.cursor()
        query = "select outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active from outages_map where report_id = %s;"
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        return result
    
    def updateOutages(self, outages_id, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active):
        cursor = self.conn.cursor()
        query = "update outages_map set report_id=%s, outage_type=%s, outage_lat=%s, outage_lng=%s, outage_source=%s, outage_date=%s, outage_company=%s, active=%s where outages_id=%s;"
        cursor.execute(query, (report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active, outages_id,))
        self.conn.commit()
        return True

    def insertOutages(self, report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active):
        cursor = self.conn.cursor()
        query = "insert into outages_map (report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active) values (%s, %s, %s, %s, %s, %s, %s, %s) returning outages_id;"
        cursor.execute(query, (report_id, outage_type, outage_lat, outage_lng, outage_source, outage_date, outage_company, active,))
        outages_id = cursor.fetchone()[0]
        self.conn.commit()
        return outages_id
    
    def deleteOutages(self, outages_id):
        cursor = self.conn.cursor()
        query = "delete from outages_map where outages_id=%s"
        cursor.execute(query, (outages_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
    
    def deleteOutagesByReportId(self, report_id):
        cursor = self.conn.cursor()
        query = "delete from outages_map where report_id=%s"
        cursor.execute(query, (report_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0