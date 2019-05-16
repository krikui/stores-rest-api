import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This username field cannot be empty'
        )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This password field cannot be empty'
    )



    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "user {} already exists".format(data["username"])}, 400
        user = UserModel(**data)
        user.save_to_db()
        # with sqlite3.connect("data.db") as connection:
        #     cursor = connection.cursor()
        #     query = "INSERT INTO {} VALUES (NULL, ?, ?)".format(self.TABLE_NAME)
        #     cursor.execute(query, (data['username'], data['password']),)
        #     connection.commit()
        #     return {"message": "user {} was created.".format(data["username"])}, 201

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query1 = "SELECT username from {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query1, )

        if result:
            rows = set()
            for row in result:
                rows.add(row[0])
        return {"message": "Users registered successfully {}.".format(rows)}, 200

        connection.commit()
        connection.close()



