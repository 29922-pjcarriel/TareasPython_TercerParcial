
import mysql.connector

def get_db_usuarios():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="usuariosdb"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to usuariosdb: {err}")
        return None

def get_db_matriculacion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="matriculacionfinal"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to matriculacionfinal: {err}")
        return None
