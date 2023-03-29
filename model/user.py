from config.dbconfig import pg_config
import psycopg2


class UserDAO:
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
                                                                            pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def login(self, user_email, user_password):
        cursor = self.conn.cursor()
        query = "select user_id from \"user\" where user_email = %s and user_password = crypt(%s, user_password)"
        cursor.execute(query, (user_email, user_password))
        user_id = cursor.fetchone()
        cursor.close()
        return user_id

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select user_name, user_email, user_phone from \"user\";"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def updateUser(self, user_password, user_email, field, change):
        cursor = self.conn.cursor()
        query = 'update \"user\" set %s = %s, updated_at = current_date where user_email = %s ' \
                'and user_password = crypt(%s, user_password)'
        cursor.execute(query, (field, change, user_email, user_password))
        self.conn.commit()
        query_show = 'select * from \"user\" where user_email = %s and user_password = crypt(%s, user_password)'
        cursor.execute(query_show, (user_email, user_password))
        result = cursor.fetchone()
        cursor.close()
        return result

    def insertUser(self, user_name, user_email, user_type, user_phone, user_password):
        cursor = self.conn.cursor()
        query = "insert into \"user\" (user_name, user_email, user_type, user_phone, " \
                "user_password, created_at, updated_at) values (%s, %s, %s, %s, crypt(%s, gen_salt('md5')), " \
                "current_date, current_date) returning user_id"
        cursor.execute(query, (user_name, user_email, user_type, user_phone, user_password))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def deleteUser(self, user_email, user_password):
        cursor = self.conn.cursor()
        query = "delete from \"user\" where user_email = %s and user_password = crypt(%s, user_password)"
        cursor.execute(query, (user_email, user_password))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0

    def checkEmails(self):
        cursor = self.conn.cursor()
        query = "select user_email from \"user\""
        cursor.execute(query)
        result = []
        for rows in cursor:
            result.append(rows)
        cursor.close()
        return result

    def checkUsernames(self):
        cursor = self.conn.cursor()
        query = "select user_name from \"user\""
        cursor.execute(query)
        result = []
        for rows in cursor:
            result.append(rows)
        cursor.close()
        return result

    def getUserbyID(self, user_id):
        cursor = self.conn.cursor()
        query = "select user_name from \"user\" where %s"
        cursor.execute(query, user_id)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
