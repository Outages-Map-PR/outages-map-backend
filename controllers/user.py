from flask import jsonify
from model.user import UserDAO

class User:
    def build_row_dict(self, row):
        if row:
            result = {
                "user_id": row[0],
                "user_name": row[1],
                "user_email": row[2],
                "user_phone": row[3],
                "user_password": row[4]
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result
    
    def build_attr_dict(self, user_id, user_name, user_email, user_phone, user_password):
        result = {}
        result['user_id'] = user_id
        result['user_name'] = user_name
        result['user_email'] = user_email
        result['user_phone'] = user_phone
        result['user_password'] = user_password
        return result
    
    def getAllUsers(self):
        dao = UserDAO()
        tuples = dao.getAllUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)