from users import User
import connection as db

class usersDAO:

    @staticmethod
    def create_user(user):
        query = "INSERT INTO users (userName, password) VALUES %s, %s"
        cursor = db.connection.cursor()
        cursor.execute(query, user.get_username(), user.get_password())
        db.connection.commit()

        return user
    
    def read_users():
        query = "SELECT * FROM users"
        cursor = db.connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        users = []
        for row in rows:
            userid = row[0]
            username = row[1]
            password = row[2]

            users.append(User(username, password, userid))
        
        return users