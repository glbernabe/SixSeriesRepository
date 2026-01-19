import uuid

import mariadb

from app.models.models import UserDb, SubscriptionDb, UserId

# ----------------------------- DATABASE CONFIG ---------------------------------
db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi" ,
    "password": "myapi" ,
    "database": "myapi"
}
# ----------------------------- USERS ----------------------------------------
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

# -------------------------- SUBSCRIPTION ---------------------------------
from datetime import date
import uuid

def add_subscription_query(user_id: str, sub_type: str, end_date:date) -> dict:
    subscription_id = str(uuid.uuid4())
    start_date = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO SUBSCRIPTION (id, userId, type, startDate, endDate)VALUES (?, ?, ?, ?, ?) "
            cursor.execute(sql,(subscription_id, user_id, sub_type, start_date, end_date))
            conn.commit()
    return {
        "id": subscription_id,
        "user_id": user_id,
        "type": sub_type,
        "startDate": start_date,
        "endDate": end_date
    }
def get_subscription_query(user_id: str) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id,startDate, endDate, status, type FROM SUBSCRIPTION WHERE userId = ?"
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()

            subscription = []
            for row in results:
                subscription.append({
                    "id": row[0],
                    "startDate": row[1],
                    "endDate": row[2],
                    "status": row[3],
                    "type": row[4]
                })
            return subscription


