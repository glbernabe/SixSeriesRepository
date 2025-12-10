from tkinter.font import names
import mariadb
from app.models import UserDb


db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi" ,
    "password": "myapi" ,
    "database": "myapi"
}

def insert_user(user:UserDb):
    # Doble asterisco transforma el diccionario en una lista de parametros/argumentos (**)
    # Por ejemplo, host="myapidb", port=3306, user="myapi"...
    with mariadb.connect(**db_config) as conn:
        # Cursor es el objeto con el que podemos usar SQL
        with conn.cursor() as cursor:
            # Primera consulta
            sql = "insert into users (username,email, password) values (?, ?, ?)"
            values = (user.username, user.email, user.password)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    for u in users:
        if u.username == username:
            return u
    return None
users: list[UserDb] = [
    UserDb(
        id=1,
        username='Alice',
        email='alice@gmail.com',
        password='$2b$12$SO1mefC/IBZ5t9qbyLTUE.hJne994Oz8wWpwQRiWC3C9yij4MYiWO'
    ),
    UserDb(
        id=2,
        username='Bob',
        email='bob@gmail.com',
        password='$2b$12$GUV8UnCTmBdzb1tDGkrUQuMaitIGuMdf.3MCLqYNwRxsE016IZq86'
    )
]
