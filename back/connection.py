import mysql.connector

connection = None

def create_connection(user, password):
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = user,
            password = password,
            database = "anime_recommendation"
        )
        return mydb
    except mysql.connector.Error as e:
        print("Error en la conexión a la base de datos:", e)

def init_connection():
    global connection
    user = input("Introduce el nombre de usuario de la Base de Datos: ")
    password = input("Introduce la contraseña a la Base de Datos: ")
    if connection is None:
        connection = create_connection(user, password)
    return connection
