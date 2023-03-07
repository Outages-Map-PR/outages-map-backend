from flask import jsonify
from model.user import UserDAO


class User:
    def build_row_dict(self, row):
        result = {
            "user_id": row[0],
            "user_name": row[1],
            "user_email": row[2],
            "user_phone": row[3],
            "user_password": row[4],
            'created_at': row[5],
            'updated_at': row[6]
        }
        return result

    def build_attr_dict(self, user_id, user_name, user_email, user_phone, user_password, created_at, updated_at):
        result = {'user_id': user_id, 'user_name': user_name, 'user_email': user_email, 'user_phone': user_phone,
                  'user_password': user_password, 'created_at': created_at, 'updated_at': updated_at}
        return result

    def login(self, json):
        dao = UserDAO()
        user_email = json["user_email"]
        user_password = json["user_password"]
        user_id = dao.login(user_email, user_password)
        if user_id:
            return jsonify(user_id), 200
        else:
            return jsonify("USER NOT FOUND"), 404

    def getAllUsers(self):
        dao = UserDAO()
        tuples = dao.getAllUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        if result:
            return jsonify(result), 200
        else:
            return jsonify("NO USERS FOUND"), 404

    def updateUser(self, json):
        dao = UserDAO()
        user_password = json["user_password"]
        user_email = json["user_email"]
        field = json["field"]
        change = json["change"]
        updated_user = dao.updateUser(user_password, user_email, field, change)
        if updated_user:
            result = self.build_row_dict(updated_user)
            return jsonify(result), 201
        return jsonify("USER NOT FOUND"), 404

    def insertUser(self, json):
        dao = UserDAO()
        user_email = json["user_email"]
        user_password = json["user_password"]
        user_name = json["user_name"]
        user_type = json["user_type"]
        user_phone = json["user_phone"]
        emails = dao.checkEmails()
        usernames = dao.checkUsernames()
        if user_email in emails or user_name in usernames:
            return jsonify("EMAIL OR USERNAME ALREADY EXISTS"), 404
        new_user = dao.insertUser(user_name, user_email, user_type, user_phone, user_password)
        if new_user:
            return jsonify(new_user), 200
        else:
            return jsonify("USER NOT CREATED"), 404

    def deleteUser(self, json):
        dao = UserDAO()
        deleted_user = dao.deleteUser(json[0], json[1])
        if deleted_user:
            return jsonify("USER DELETION COMPLETE"), 200
        else:
            return jsonify("USER NOT FOUND"), 404
