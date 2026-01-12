import mariadb
from app.models.models import UserDb


db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root" ,
    "password": "root" ,
    "database": "myapi"
}

def insert_user(user:UserDb):
    # Doble asterisco transforma el diccionario en una lista de parametros/argumentos (**)
    # Por ejemplo, host="myapidb", port=3306, user="myapi"...
    with mariadb.connect(**db_config) as conn:
        # Cursor es el objeto con el que podemos usar SQL
        with conn.cursor() as cursor:
            # Primera consulta
            sql = "insert into USER (id, username, password, email) values (?, ?, ?, ?)"
            values = (str(user.id), user.username, user.password, user.email)
            cursor.execute(sql, values)
            conn.commit()
            return user.id


def get_user_by_id(id_user: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email FROM USER WHERE id = ?"
            cursor.execute(sql, (id_user,))
            row = cursor.fetchone()
            if row is None:
                return None
            return UserDb(id=str(row[0]), username=row[1], password=row[2], email=row[3])
        
        
def get_all_users_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email FROM USER"
            cursor.execute(sql)
            rows = cursor.fetchall()

            users = []
            for row in rows:
                users.append(
                    UserDb(id=row[0],username=row[1],password=row[2],email=row[3])
                )
            return users

def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email FROM `USER` WHERE username = ?"
            values = (username,)
            cursor.execute(sql, values)

            row = cursor.fetchone()
            if row:
                return UserDb(id=row[0], username=row[1], password=row[2], email=row[3])
            return None

def get_all_content_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM `CONTENT`"
            cursor.execute(sql)
            rows = cursor.fetchall()

            titles = []
            for row in rows:
                titles.append(row)
            return titles
