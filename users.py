import psycopg2
from psycopg2 import sql

def get_users(connection):
    with connection.cursor() as cursor:
        query = sql.SQL("SELECT usename FROM pg_user;")
        cursor.execute(query)
        users = cursor.fetchall()
    return users

def login_as_user(user, password, dbname='TAB', host='localhost', port=5432):
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return connection

admin_connection = psycopg2.connect(
    dbname='TAB',
    user='administrator',
    password='12345',
    host='localhost',
    port=5432
)




