from users import User
import connection as db

class usersDAO:

    @staticmethod
    def create_user(user):
        query = "INSERT INTO users (username, password) VALUES %s, %s"
        cursor = db.connection.cursor()
        cursor.execute(query, user.get_username(), user.get_password())
        db.connection.commit()

        return user