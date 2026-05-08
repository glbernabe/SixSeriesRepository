import uuid
from fastapi import HTTPException

import mariadb
from starlette import status
from datetime import date, timedelta
from app.models.models import UserDb, SubscriptionDb, UserId, SubscriptionOut, ProfileOut, PaymentOut, ContentDb, \
    ContentUser, Genre, RatingValue, UserOut, HistoryOut, PaymentType

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
def change_password_query(hashed: str, new_password: str, new_password_retype: str, username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email FROM USER WHERE username = ? "
            cursor.execute(sql, (username,))
            rows = cursor.fetchone()
            passwd = rows[2]
            if passwd == new_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Your password is the same."
                )
            if new_password != new_password_retype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password and password retype doesnt coincide.."
                )
            sql = "UPDATE USER SET password = ? WHERE username = ?"
            cursor.execute(sql, (hashed, username))
            conn.commit()

            return {"message": "Password changed."}

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
from datetime import date, datetime
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
def create_profile_query(user_username: str, name: str, color: str):
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
            sql_exists = """
                         SELECT 1 FROM PROFILE
                         WHERE userUsername = ? AND name = ? \
                         """
            cursor.execute(sql_exists, (user_username, name))
            exists = cursor.fetchone()

            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This profile already exists"
                )


            sql_insert = "INSERT INTO PROFILE (id, userUsername, name, profileColor) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_insert, (profile_id, user_username, name, color))
            conn.commit()
            sql_select_profile = "SELECT id, userUsername, name FROM PROFILE WHERE id = ?"
            cursor.execute(sql_select_profile,(profile_id,))
            conn.commit()

            return {"name": name, "profileColor": color}
def change_profile_name_query(user_username: str, old_name: str, new_name: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_check = """
                        SELECT id FROM PROFILE
                        WHERE userUsername = ? AND name = ? \
                        """
            cursor.execute(sql_check, (user_username, old_name))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(
                    status_code=404,
                    detail="Profile not found"
                )

            sql_exists = """
                         SELECT 1 FROM PROFILE
                         WHERE userUsername = ? AND name = ? \
                         """
            cursor.execute(sql_exists, (user_username, new_name))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=409,
                    detail="Profile name already exists"
                )
            sql_update = """
                         UPDATE PROFILE
                         SET name = ?
                         WHERE userUsername = ? AND name = ? \
                         """
            cursor.execute(sql_update, (new_name, user_username, old_name))
            conn.commit()
            return {"old_name": old_name, "new_name": new_name}

def delete_profile_query(user_username: str, name:str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_exists = """
                         SELECT 1 FROM PROFILE
                         WHERE userUsername = ? AND name = ? \
                         """
            cursor.execute(sql_exists, (user_username, name))
            exists = cursor.fetchone()

            if not exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This profile doesnt exists"
                )

            idProfile = exists[0]
            sql = "DELETE FROM PROFILE WHERE userUsername = ? AND name = ?"
            cursor.execute(sql, (user_username, name))
            conn.commit()
            sql_history = "DELETE FROM HISTORY WHERE profileId = ?"
            cursor.execute(sql_history, (idProfile,))
            conn.commit()
            return {"name": name}

def change_profile_color_query(user_username: str, name: str, color: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE PROFILE SET profileColor=? WHERE userUsername = ? AND name = ?"
            cursor.execute(sql, (color, user_username, name))
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El perfil no existe o no pertenece a esta cuenta."
                )
        conn.commit()
        return {"name": name, "profileColor": color}
def get_profiles_query(user_username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT name, profileColor FROM PROFILE WHERE userUsername = ?"
            cursor.execute(sql, (user_username,))
            rows = cursor.fetchall()

            names = []
            for row in rows:
                names.append(
                    ProfileOut(name=row[0], profileColor=row[1])
                )
            return names

# ------------------------ SUPERUSER -------------------------------------
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
def confirm_payment_query(user_username, method: PaymentType) -> PaymentOut:
    id = str(uuid.uuid4())
    paymentDate = date.today()

    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_select = """
                         SELECT id, type, status
                         FROM SUBSCRIPTION
                         WHERE userUsername = ? \
                         """
            cursor.execute(sql_select, (user_username,))
            row = cursor.fetchone()

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User does not have a subscription"
                )

            SubscriptionId = row[0]
            Subscription_type = row[1]
            Subscription_status = row[2]

            if Subscription_status == "active":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have active the subscription"
                )

            price_map = {
                "standard": 9.99,
                "standard_yearly": 99.99,
                "premium": 14.59,
                "premium_yearly": 140.59
            }

            if Subscription_type not in price_map:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid subscription type"
                )

            amount = price_map[Subscription_type]

            sql_insert = """
                         INSERT INTO PAYMENT
                             (id, subscriptionId, paymentDate, method, amount)
                         VALUES (?,?,?,?,?) \
                         """
            cursor.execute(sql_insert, (id, SubscriptionId, paymentDate, method, amount))

            sql_update = """
                         UPDATE SUBSCRIPTION
                         SET status = 'active'
                         WHERE id = ? \
                         """
            cursor.execute(sql_update, (SubscriptionId,))

            conn.commit()

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
def cancel_payment_query(payment_id: str, user_username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_check = """
                        SELECT p.subscriptionId
                        FROM PAYMENT p
                                 JOIN SUBSCRIPTION s ON p.subscriptionId = s.id
                        WHERE p.id = ? AND s.userUsername = ? \
                        """
            cursor.execute(sql_check, (payment_id, user_username))
            row = cursor.fetchone()

            if not row:
                raise HTTPException(404, "Payment not found")

            subscription_id = row[0]

            sql_delete_subscription = """
                                      DELETE FROM SUBSCRIPTION
                                      WHERE id = ? \
                                      """
            cursor.execute(sql_delete_subscription, (subscription_id,))

            conn.commit()

            return {"payment_id": payment_id, "subscription_deleted": subscription_id}

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
# Añadir al SELECT:
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
                      type,
                      uploadDate,
                      releaseDate
                  FROM CONTENT \
                  """
            cursor.execute(sql)
            return cursor.fetchall()



def get_content_by_title_query(title: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = sql = """
                        SELECT title, description, duration, ageRating, coverUrl, videoUrl, type, uploadDate, releaseDate
                        FROM CONTENT
                        WHERE title = ?"""
            values = (title,)
            cursor.execute(sql, values)

            row = cursor.fetchone()
            if row:
                return ContentUser(title=row[0], description=row[1], duration=row[2],
                                   age_rating=row[3], cover_url=row[4], video_url=row[5],
                                   type=row[6], uploadDate=row[7], releaseDate=row[8])
            return None


def create_content_query(content: ContentDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            uploadDate = date.today()
            sql = "INSERT INTO CONTENT (id, title, description, duration, ageRating, coverUrl, videoUrl, type, uploadDate, releaseDate) values (?,?,?,?,?,?,?,?,?,?)"
            values = (content.id, content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type, uploadDate,  content.releaseDate)
            cursor.execute(sql, values)
            conn.commit()


def modify_content_query(content: ContentUser, id_content: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTENT SET title=?, description=?, duration=?, ageRating=?, coverUrl=?, videoUrl=?, type=?, releaseDate =? WHERE id=?"
            values = (content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type, id_content, content.releaseDate)
            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                raise HTTPException(404, "Content not found")
            conn.commit()
            return get_content_by_title_query(content.title)

def delete_content_query(content_id: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_check = "SELECT 1 FROM CONTENT WHERE id = ?"
            cursor.execute(sql_check, (content_id,))
            if not cursor.fetchone():
                raise HTTPException(404, "Content not found")

            sql_delete = "DELETE FROM CONTENT WHERE id = ?"
            cursor.execute(sql_delete, (content_id,))
            conn.commit()

            return {"deleted_content_id": content_id}

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

# ------------------------ RATING -------------------------
def rate_content_query(content_name:str, profile_name :str, RatingValue: RatingValue, username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_content = "SELECT id FROM CONTENT WHERE title = ?"
            cursor.execute(sql_content, (content_name,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="That content doesnt exist."
                )
            idContent = row[0]
            sql_profile = """
                          SELECT id
                          FROM PROFILE
                          WHERE name = ? AND userUsername = ? \
                          """
            cursor.execute(sql_profile, (profile_name, username))
            row1 = cursor.fetchone()

            if row1 is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="That profile does not belong to this user."
                )
            idProfile = row1[0]

            sql_rating = """
                         SELECT 1 FROM RATING
                         WHERE profileId = ? AND contentId = ? \
                         """
            cursor.execute(sql_rating, (idProfile, idContent))
            exists = cursor.fetchone()

            if exists:
                sql_update = """
                             UPDATE RATING
                             SET rating = ?
                             WHERE profileId = ? AND contentId = ? \
                             """
                cursor.execute(
                    sql_update,
                    (RatingValue.value, idProfile, idContent)
                )
            else:
                sql_insert = """
                             INSERT INTO RATING (profileId, contentId, rating)
                             VALUES (?, ?, ?) \
                             """
                cursor.execute(
                    sql_insert,
                    (idProfile, idContent, RatingValue.value)
                )

            conn.commit()

def get_rates_query(profile_name: str, username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_profile = """
                          SELECT id
                          FROM PROFILE
                          WHERE name = ? AND userUsername = ? \
                          """
            cursor.execute(sql_profile, (profile_name, username))
            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="That profile does not belong to this user."
                )

            idProfile = row[0]

            sql = """
                  SELECT c.title, r.rating
                  FROM RATING r
                           JOIN CONTENT c ON r.contentId = c.id
                  WHERE r.profileId = ? \
                  """
            cursor.execute(sql, (idProfile,))
            rates = cursor.fetchall()

            return rates




def upsert_history_query(profile_name: str, content_title: str, time_viewed: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_profile = "SELECT id FROM PROFILE WHERE name = ?"
            cursor.execute(sql_profile, (profile_name,))
            row_profile = cursor.fetchone()
            if not row_profile:
                raise HTTPException(404, "Profile not found")
            profile_id = row_profile[0]

            sql_content = "SELECT id FROM CONTENT WHERE title = ?"
            cursor.execute(sql_content, (content_title,))
            row_content = cursor.fetchone()
            if not row_content:
                raise HTTPException(404, "Content not found")
            content_id = row_content[0]

            sql_check = """
                        SELECT 1 FROM HISTORY
                        WHERE profileId = ? AND contentId = ? \
                        """
            cursor.execute(sql_check, (profile_id, content_id))
            exists = cursor.fetchone()

            now = datetime.now()

            if exists:
                sql_update = """
                             UPDATE HISTORY
                             SET lastWatched = ?, timeViewed = ?
                             WHERE profileId = ? AND contentId = ? \
                             """
                cursor.execute(sql_update, (now, time_viewed, profile_id, content_id))
            else:
                sql_insert = """
                             INSERT INTO HISTORY (profileId, contentId, lastWatched, timeViewed)
                             VALUES (?, ?, ?, ?) \
                             """
                cursor.execute(sql_insert, (profile_id, content_id, now, time_viewed))

            conn.commit()

def get_history_query(profile_name: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_profile = "SELECT id FROM PROFILE WHERE name = ?"
            cursor.execute(sql_profile, (profile_name,))
            row_profile = cursor.fetchone()
            if not row_profile:
                raise HTTPException(status_code=404, detail="Profile not found")
            profile_id = row_profile[0]
            sql_select = """
                         SELECT c.title, h.lastWatched, h.timeViewed
                         FROM HISTORY h
                                  JOIN CONTENT c ON h.contentId = c.id
                         WHERE h.profileId = ? \
                         """
            cursor.execute(sql_select, (profile_id,))
            rows = cursor.fetchall()

            history = [
                HistoryOut(
                    title=row[0],
                    lastWatched=row[1],
                    timeViewed=row[2]
                )
                for row in rows
            ]

            return history

# Endpoint para obtener ultimas peliculas en las ultimas 2 semanas, si no hay, se mostraran dos semanas en adelante.
# Con un maximo de 10
def get_latest_content_query():
    content_list = []
    semanas_atras = 2
    limite_semanas = 52 # Por si no existieran semanas para no hacer un bucle infinito
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            while len(content_list) < 10 and semanas_atras <= limite_semanas:
                hoy = date.today()
                fecha_inicio = hoy - timedelta(weeks=semanas_atras)
                sql_select = """SELECT title, description, duration, ageRating, coverUrl, videoUrl, type, uploadDate, releaseDate FROM CONTENT where uploadDate BETWEEN %s AND %s ORDER BY uploadDate LIMIT 10 \ """
                cursor.execute(sql_select,  (fecha_inicio, hoy))
                resultados = cursor.fetchall()
                if len(content_list) < 10:
                    semanas_atras += 2
                else:
                    break
            return resultados[:10]

