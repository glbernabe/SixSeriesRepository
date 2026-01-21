import uuid
from http.client import HTTPException

import mariadb

from app.models.models import UserDb, SubscriptionDb, UserId, SubscriptionOut, ProfileOut

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

def cancel_subscription_query(user_id: str) -> SubscriptionOut | None:
    today = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, status = ? WHERE userId = ? AND status = 'active'"
            cursor.execute(sql, (today,'expired', user_id))
            conn.commit()
            if cursor.rowcount == 0:
                return None
            sql_select = "SELECT type, startDate, endDate, status FROM SUBSCRIPTION WHERE userId = ? AND status = 'expired' ORDER BY endDate DESC LIMIT 1"
            cursor.execute(sql_select, (user_id,))
            row = cursor.fetchone()

        return SubscriptionOut(
            type=row['type'],
            startDate=row['startDate'],
            endDate=row['endDate'],
            status=row['status']
        )

def has_active_subscription(user_id:str, family:str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT COUNT(*) as count FROM SUBSCRIPTION WHERE userId = ? AND status = 'active' AND (type = ? OR type = ?)"
                if family == "standard":
                    cursor.execute(sql, (user_id, "standard", "standard_yearly"))
                else:
                    cursor.execute(sql, (user_id, "premium", "premium_yearly"))
                row = cursor.fetchone()
                return row['count'] > 0

def update_subscription_query(user_id:str, new_type:str, endDate:date) -> SubscriptionOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, type = ? WHERE userId = ?"
            cursor.execute(sql, (endDate, new_type, user_id))
            conn.commit()

            sql_select = "SELECT type, startDate, endDate, status FROM SUBSCRIPTION WHERE userId = ? AND status = 'active' ORDER BY endDate DESC LIMIT 1"
            cursor.execute(sql_select, (user_id,))
            row = cursor.fetchone()

        return SubscriptionOut(
            type=row['type'],
            startDate=row['startDate'],
            endDate=row['endDate'],
            status=row['status']
        )
# ---------------------------- PROFILE ----------------------------------
def create_profile_query(user_id: str, name: str):
    profile_id = str(uuid.uuid4())
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_select = "SELECT 1 FROM SUBSCRIPTION WHERE userId = ? AND status = 'active'"
            cursor.execute(sql_select,(user_id,))
            sub = cursor.fetchone()
            if not sub:
                raise Exception("User has no active subscription")
            sql_count = "SELECT COUNT(*) FROM PROFILE WHERE userId = ?"
            cursor.execute(sql_count( user_id,))
            count = cursor.fetchone()[0]
            if count >= 5:
                raise Exception("User cannot have more than 5 profiles")
            sql_insert = "INSERT INTO PROFILE (id, userId, name) VALUES (?, ?, ?)"
            cursor.execute(sql_insert,(profile_id, user_id, name))
            conn.commit()
            sql_select_profile = "SELECT id, userId, name FROM PROFILE WHERE id = ?"
            cursor.execute(sql_select_profile,(profile_id,))
            conn.commit()

            return {"name": name}

#def delete_profile_query(user_id: str, name:str)
# ------------- SUPERUSER -------------------------------------
def get_superuser_permissions(user_id: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT permissions FROM SUPERUSER WHERE id = ?"
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return row[0]