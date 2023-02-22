from config.dbconfig import pg_config
# import psycopg2

class UserDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
        pg_config['user'], pg_config['password'],pg_config['port'], pg_config['host'])
        # self.conn = psycopg2.connect(connection_url)
        
    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, user_email, user_phone, user_password from \"user\";"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getUserById(self, user_id):
        pass
    
    def updateUser(self, user_id, user_name, user_email, user_type, user_phone, user_password):
        pass
    
    def insertUser(self, user_name, user_email, user_type, user_phone, user_password):
        pass
    
    def deleteUser(self, user_id):
        pass