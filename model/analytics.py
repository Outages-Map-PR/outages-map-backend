from config.dbconfig import pg_config
import psycopg2

# Definitions
POWER = 'power'
WATER = 'water'
INTERNET = 'internet'

class analyticsDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
                                                                            pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)  
            
    def getServiceAnalytics(self, date, outage_type):
        # Date is formatted yyyy-mm
        # outage_type: POWER, WATER, INTERNET
        cursor = self.conn.cursor()
        query = "SELECT * FROM outages_map WHERE to_char(outage_date, 'yyyy-mm') = %s AND outage_type = %s"
        if outage_type == POWER:
            cursor.execute(query, (date, POWER))
        elif outage_type == WATER:
            cursor.execute(query, (date, WATER))
        elif outage_type == INTERNET:
            cursor.execute(query, (date, INTERNET))
        else: 
            return({'error': 'Wrong outage_type defined.'})
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAllAnalytics(self, date):
        # Date is formatted yyyy-mm
        power_t = self.getServiceAnalytics(date, POWER)
        water_t = self.getServiceAnalytics(date, WATER)
        internet_t = self.getServiceAnalytics(date, INTERNET)
        return (power_t, water_t, internet_t)
    
    def getAnalyticsDayCount(self, date, outage_type):
        # Date is formatted yyyy-mm
        # outage_type: POWER, WATER, INTERNET
        cursor = self.conn.cursor()
        query = """
            SELECT DATE_TRUNC('day', outage_date)::DATE AS daily_date,
            COUNT(*) AS report_count
            FROM outages_map
            WHERE to_char(outage_date, 'yyyy-mm') = %s
            AND outage_type = %s
            GROUP BY DATE_TRUNC('day', outage_date)
            ORDER BY DATE_TRUNC('day', outage_date)
        """
        if outage_type == POWER:
            cursor.execute(query, (date, POWER))
        elif outage_type == WATER:
            cursor.execute(query, (date, WATER))
        elif outage_type == INTERNET:
            cursor.execute(query, (date, INTERNET))
        else: 
            return({'error': 'Wrong outage_type defined.'})
        result = cursor.fetchall()
        return result