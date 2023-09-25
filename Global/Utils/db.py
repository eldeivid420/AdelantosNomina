import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
DATABASE_NAME = os.environ.get('DB_NAME')
DATABASE_USER = os.environ.get('DB_USER')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE_HOST = os.environ.get('DB_HOST')
DATABASE_PORT = os.environ.get('DB_PORT')
conn = psycopg2.connect(
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
)


def post(query, params, returns = False):
    """
    Método que ejecuta escritura sobre la pase de datos
    :param query: el Query string
    :param params: una tupla de parametros para insertar en el query
    :param returns: True si debe regresar algo
    :return:
    """
    try:
        conn.rollback()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if returns:
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return e

def get(query, params, fetchAll=True):
    """
    Método que ejecuta una consulta a la base de datos
    :param query: el Query string
    :param params: una tupla de parámetros a insertar en el query
    :param fetch: True si se va a regresar toda la tupla de resultados. False si se regresa solo un elemento.
    :return: Toda la tupla o un elemento.
    """
    try:
        conn.rollback()
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetchAll:
            return cursor.fetchall()
        else:
            return cursor.fetchone()
    except Exception as e:
        print(e)
        return e