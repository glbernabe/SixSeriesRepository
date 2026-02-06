import uuid
from fastapi import HTTPException

import mariadb
from starlette import status

from app.models.models import UserDb, SubscriptionDb, UserId, SubscriptionOut, ProfileOut, PaymentOut, ContentDb, ContentUser, Genre
# ----------------------------- DATABASE CONFIG ---------------------------------
db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "root" ,
    "password": "root" ,
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

def add_subscription_query(user_username: str, sub_type: str, end_date:date) -> dict:
    subscription_id = str(uuid.uuid4())
    start_date = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO SUBSCRIPTION (id, userUsername, type, startDate, endDate)VALUES (?, ?, ?, ?, ?) "
            cursor.execute(sql, (subscription_id, user_username, sub_type, start_date, end_date))
            conn.commit()
    return {
        "id": subscription_id,
        "user_username": user_username,
        "type": sub_type,
        "startDate": start_date,
        "endDate": end_date
    }
def get_subscription_query(user_username: str) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id,startDate, endDate, status, type FROM SUBSCRIPTION WHERE userUsername = ?"
            cursor.execute(sql, (user_username,))
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

def cancel_subscription_query(user_username: str) -> SubscriptionOut | None:
    today = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, status = ? WHERE userUsername = ? AND status = 'active'"
            cursor.execute(sql, (today,'expired', user_username))
            conn.commit()
            if cursor.rowcount == 0:
                return None
            sql_select = "SELECT type, startDate, endDate, status FROM SUBSCRIPTION WHERE userUsername = ? AND status = 'expired' ORDER BY endDate DESC LIMIT 1"
            cursor.execute(sql_select, (user_username,))
            row = cursor.fetchone()
        return SubscriptionOut(
            type=row['type'],
            startDate=row['startDate'],
            endDate=row['endDate'],
            status=row['status']
        )

def has_active_subscription(user_username:str, family:str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT COUNT(*) as count FROM SUBSCRIPTION WHERE userUsername = ? AND status = 'active' AND (type = ? OR type = ?)"
                if family == "standard":
                    cursor.execute(sql, (user_username, "standard", "standard_yearly"))
                else:
                    cursor.execute(sql, (user_username, "premium", "premium_yearly"))
                row = cursor.fetchone()
                return row['count'] > 0

def update_subscription_query(user_username:str, new_type:str, endDate:date) -> SubscriptionOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, type = ? WHERE userUsername = ?"
            cursor.execute(sql, (endDate, new_type, user_username))
            conn.commit()

            sql_select = "SELECT type, startDate, endDate, status FROM SUBSCRIPTION WHERE userUsername = ? AND status = 'active' ORDER BY endDate DESC LIMIT 1"
            cursor.execute(sql_select, (user_username,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ypu dont have an active subscription"
                )
        return SubscriptionOut(
            type=row['type'],
            startDate=row['startDate'],
            endDate=row['endDate'],
            status=row['status']
        )
# ---------------------------- PROFILE ----------------------------------
def create_profile_query(user_username: str, name: str):
    profile_id = str(uuid.uuid4())
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_select = "SELECT 1 FROM SUBSCRIPTION WHERE userUsername = ? AND status = 'active'"
            cursor.execute(sql_select, (user_username,))
            sub = cursor.fetchone()
            if not sub:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User has no active subscription"
                )
            sql_count = "SELECT COUNT(*) FROM PROFILE WHERE userUsername = ?"
            cursor.execute(sql_count, (user_username,))
            count = cursor.fetchone()[0]
            if count >= 5:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User cannot have more than 5 profiles"
                )
            sql_limit = "SELECT name FROM PROFILE where userUsername = ?"
            cursor.execute(sql_limit, (user_username,))
            row = cursor.fetchone()
            name_db = row[0]
            if name_db == name:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This profile already exists"
                )
            sql_insert = "INSERT INTO PROFILE (id, userUsername, name) VALUES (?, ?, ?)"
            cursor.execute(sql_insert, (profile_id, user_username, name))
            conn.commit()
            sql_select_profile = "SELECT id, userUsername, name FROM PROFILE WHERE id = ?"
            cursor.execute(sql_select_profile,(profile_id,))
            conn.commit()

            return {"name": name}

def delete_profile_query(user_username: str, name:str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM PROFILE WHERE userUsername = ? AND name = ?"
            cursor.execute(sql, (user_username, name))
            conn.commit()

            return {"name": name}
def get_profiles_query(user_username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT name FROM PROFILE WHERE userUsername = ?"
            cursor.execute(sql, (user_username,))
            rows = cursor.fetchall()

            names = []
            for row in rows:
                names.append(
                    ProfileOut(name=row[0])
                )
            return names
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


# ------------ PAYMENTS -----------------
def confirm_payment_query(user_username, method:str) -> PaymentOut :
    id = str(uuid.uuid4())
    paymentDate = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_select = "SELECT id, type, status FROM SUBSCRIPTION WHERE userUsername = ?"
            cursor.execute(sql_select,(user_username,))
            row = cursor.fetchone()
            SubscriptionId = row[0]
            Subscription_type = row[1]
            Subscription_status = row[2]
            if Subscription_status == "active":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have active the subscription"
                )
            #standard = 9.99
            #standard_yearly = 99.99
            #premium = 14.59
            #premium_yearly = 140.59
            if Subscription_type == "standard":
                amount = 9.99
                sql_insert = "INSERT INTO PAYMENT (id, subscriptionId, paymentDate, method, amount) VALUES (?,?,?,?,?)"
                cursor.execute(sql_insert, (id, SubscriptionId, paymentDate, method,amount ))
                conn.commit()
                sql_update = "UPDATE SUBSCRIPTION SET status = 'active' WHERE userUsername = ?"
                cursor.execute(sql_update,(user_username,))
                conn.commit()
            elif Subscription_type == "standard_yearly":
                amount = 99.99
                sql_insert = "INSERT INTO PAYMENT (id, subscriptionId, paymentDate, method, amount) VALUES (?,?,?,?,?)"
                cursor.execute(sql_insert, (id, SubscriptionId, paymentDate, method,amount ))
                conn.commit()
                sql_update = "UPDATE SUBSCRIPTION SET status = 'active' WHERE userUsername = ?"
                cursor.execute(sql_update,(user_username,))
                conn.commit()
            elif Subscription_type == "premium":
                amount = 14.59
                sql_insert = "INSERT INTO PAYMENT (id, subscriptionId, paymentDate, method, amount) VALUES (?,?,?,?,?)"
                cursor.execute(sql_insert, (id, SubscriptionId, paymentDate, method,amount ))
                conn.commit()
                sql_update = "UPDATE SUBSCRIPTION SET status = 'active' WHERE userUsername = ?"
                cursor.execute(sql_update,(user_username,))
                conn.commit()
            elif Subscription_type == "premium_yearly":
                amount = 140.59
                sql_insert = "INSERT INTO PAYMENT (id, subscriptionId, paymentDate, method, amount) VALUES (?,?,?,?,?)"
                cursor.execute(sql_insert, (id, SubscriptionId, paymentDate, method,amount ))
                conn.commit()
                sql_update = "UPDATE SUBSCRIPTION SET status = 'active' WHERE userUsername = ?"
                cursor.execute(sql_update,(user_username,))
                conn.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You dont have a Subscription"
                )
        return PaymentOut(
            paymentDate=paymentDate,
            method=method,
            amount=amount
        )
def get_payments_query(user_username) -> PaymentOut:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql_select = "SELECT id FROM SUBSCRIPTION WHERE userUsername = ?"
            cursor.execute(sql_select,(user_username,))
            row = cursor.fetchone()
            if not row:
                return None
            SubscriptionId = row['id']
            sql_select = "SELECT paymentDate, method, amount FROM PAYMENT WHERE subscriptionId = ?"
            cursor.execute(sql_select, (SubscriptionId,))
            row2 = cursor.fetchone()
        return PaymentOut(
            paymentDate=row2['paymentDate'],
            method= row2['method'],
            amount=row2['amount']
        )
# Verificar que hay un superusuario con el nombre de usuario que se pasa
def verify_superuser(username: str) -> bool | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            user = get_user_by_username(username)

            sql = "SELECT id FROM `SUPERUSER` WHERE id = ?"
            values = (user.id,)
            cursor.execute(sql, values)

            row = cursor.fetchone()

            if not row:
                raise HTTPException(403, "You are not allowed")


# ---------------------- CONTENT ----------------------

def get_all_content_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
                  SELECT
                      title,
                      description,
                      duration,
                      ageRating AS age_rating,
                      coverUrl  AS cover_url,
                      videoUrl  AS video_url,
                      type
                  FROM CONTENT \
                  """
            cursor.execute(sql)
            return cursor.fetchall()



def get_content_by_title_query(title: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = sql = """
                        SELECT title, description, duration, ageRating, coverUrl, videoUrl, type
                        FROM CONTENT
                        WHERE title = ?"""
            values = (title,)
            cursor.execute(sql, values)

            row = cursor.fetchone()
            if row:
                return ContentUser(title=row[0], description=row[1], duration=row[2],
                                   age_rating=row[3], cover_url=row[4], video_url=row[5],
                                   type=row[6])
            return None


def create_content_query(content: ContentDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO CONTENT (id, title, description, duration, ageRating, coverUrl, videoUrl, type) values (?,?,?,?,?,?,?,?)"
            values = (content.id, content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type)
            cursor.execute(sql, values)
            conn.commit()


def modify_content_query(content: ContentUser, id_content: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTENT SET title=?, description=?, duration=?, ageRating=?, coverUrl=?, videoUrl=?, type=? WHERE id=?"
            values = (content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type, id_content)
            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                raise HTTPException(404, "Content not found")
            conn.commit()
            return get_content_by_title_query(content.title)

# ---------------------- GENRE ----------------------
def get_all_genres_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT name FROM GENRE"
            cursor.execute(sql)
            row = str(cursor.fetchall())

            if cursor.rowcount == 0:
                raise HTTPException(404, "There are no genres")
            conn.commit()
            return row

def create_genre_query(new_genre: Genre):
    verify_if_genre_exists(new_genre.name)

    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO GENRE (id, name) values (?, ?)"
            values = (new_genre.id, new_genre.name)
            cursor.execute(sql, values)


            conn.commit()



def verify_if_genre_exists(name_genre: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM GENRE WHERE name = ?"
            cursor.execute(sql, (name_genre,))
            row = cursor.fetchone()

            if row:
                raise HTTPException(403, "Genre already exists")
# ----------------------- FAVORITOS ----------------------------
def add_favorite_query(content_name: str, user_name: str, addedDate: date):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id FROM CONTENT WHERE title = ?"
            cursor.execute(sql, (content_name,))
            row = cursor.fetchone()
            idContent = row[0]
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="That content doesnt exist."
                )
            sql_profile = "SELECT id, userUsername, name FROM PROFILE WHERE userUsername = ?"
            cursor.execute(sql_profile, (user_name,))
            row1 = cursor.fetchone()
            idProfile = row1[0]
            sql_insert = "INSERT INTO FAVORITE (profileId, contentId, addedDate) values (?, ?, ?)"
            values = (idProfile, idContent, addedDate)
            cursor.execute(sql_insert, values)
            conn.commit()
            return {"Content name:": content_name,
                    "AddedDate": addedDate}
def remove_favorite_query(content_name:str, user_name: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_select = "SELECT id FROM CONTENT WHERE title = ?"
            cursor.execute(sql_select, (content_name,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="That content doesnt exist."
                )
            idContent = row[0]
            sql_profile = "SELECT id, userUsername, name FROM PROFILE WHERE userUsername = ?"
            cursor.execute(sql_profile, (user_name,))
            row1 = cursor.fetchone()
            idProfile = row1[0]
            sql = "DELETE FROM FAVORITE WHERE profileId = ? AND contentId = ?"
            cursor.execute(sql, (idProfile, idContent,))
            conn.commit()
            return {"Content name deleted from favorites:": content_name}
