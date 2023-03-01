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
                "user_password": row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result

    def build_attr_dict(self, user_id, user_name, user_email, user_phone, user_password, created_at, updated_at):
        result = {'user_id': user_id, 'user_name': user_name, 'user_email': user_email, 'user_phone': user_phone,
                  'user_password': user_password, 'created_at': created_at, 'updated_at': updated_at}
        return result

    def login(self, json):
        dao = UserDAO()
        user_id = dao.login(json[0], json[1])
        if user_id:
            return 200, jsonify(user_id)
        else:
            return 404, jsonify("USER NOT FOUND")

    def getAllUsers(self):
        dao = UserDAO()
        tuples = dao.getAllUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def updateUser(self, json):
        dao = UserDAO()
        updated_user = dao.updateUser(json[0], json[1], json[2], json[3])
        result = self.build_row_dict(updated_user)
        return result

    def insertUser(self, json):
        dao = UserDAO()
        new_user = dao.insertUser(json[0], json[1], json[2], json[3], json[4])
        if new_user:
            return 200, jsonify(new_user)
        else:
            return 404, jsonify("USER NOT FOUND")

    def deleteUser(self, json):
        dao = UserDAO()
        deleted_user = dao.deleteUser(json[0], json[1])
        if deleted_user:
            return 200, jsonify("USER DELETION COMPLETE")
        else:
            return 400, jsonify("USER NOT FOUND")
