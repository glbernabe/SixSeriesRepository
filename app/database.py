import uuid
from fastapi import HTTPException

import mariadb
from starlette import status
from datetime import date, timedelta, datetime
from app.models.models import UserDb, SubscriptionDb, UserId, SubscriptionOut, ProfileOut, PaymentOut, ContentDb, \
    ContentUser, Genre, RatingValue, UserOut, HistoryOut, PaymentType, EpisodeBase, EpisodeDb

# ----------------------------- DATABASE CONFIG ---------------------------------
db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "root" ,
    "password": "root" ,
    "database": "myapi"
}
# ----------------------------- USERS ----------------------------------------
def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO USER (id, username, password, email, rol, permissions) VALUES (?, ?, ?, ?, ?, ?)"
            values = (str(user.id), user.username, user.password, user.email, user.rol, user.permissions)
            cursor.execute(sql, values)
            conn.commit()
            return user.id

def get_user_by_id(id_user: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email, rol, permissions FROM USER WHERE id = ?"
            cursor.execute(sql, (id_user,))
            row = cursor.fetchone()
            if not row: return None
            return UserDb(id=str(row[0]), username=row[1], password=row[2], email=row[3], rol=row[4], permissions=row[5])
        
def get_all_users_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, email, rol, permissions FROM USER"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [UserDb(id=r[0], username=r[1], password=r[2], email=r[3], rol=r[4], permissions=r[5]) for r in rows]
        
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
            sql = "SELECT id, username, password, email, rol, permissions FROM `USER` WHERE username = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return UserDb(id=row[0], username=row[1], password=row[2], email=row[3], rol=row[4], permissions=row[5])
            return None

# -------------------------- SUBSCRIPTION ---------------------------------

def add_subscription_query(user_username: str, sub_type: str, end_date: date) -> dict:
    subscription_id = str(uuid.uuid4())
    start_date = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Database columns are camelCase
            sql = "INSERT INTO SUBSCRIPTION (id, userUsername, type, startDate, endDate, status) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (subscription_id, user_username, sub_type, start_date, end_date, "pending"))
            conn.commit()
    return {
        "id": subscription_id,
        "user_username": user_username,
        "type": sub_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": "pending"
    }

def get_subscription_query(user_username: str) -> dict:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
                SELECT 
                    id, 
                    userUsername AS user_username, 
                    type, 
                    startDate AS start_date, 
                    endDate AS end_date, 
                    status 
                FROM SUBSCRIPTION 
                WHERE userUsername = ? 
                ORDER BY startDate DESC LIMIT 1
            """
            cursor.execute(sql, (user_username,))
            row = cursor.fetchone()
            
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User doesnt hava a subscription yet."
                )
                
            if row['end_date'] < date.today() and row['status'] == 'active':
                row['status'] = 'expired'
                
            return row

def cancel_subscription_query(user_username: str) -> SubscriptionOut | None:
    today = date.today()
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, status = ? WHERE userUsername = ? AND status = 'active'"
            cursor.execute(sql, (today, 'expired', user_username))
            conn.commit()
            
            if cursor.rowcount == 0:
                return None
                
            sql_select = """
                SELECT 
                    id, 
                    type, 
                    startDate AS start_date, 
                    endDate AS end_date, 
                    status, 
                    userUsername AS user_username 
                FROM SUBSCRIPTION 
                WHERE userUsername = ? AND status = 'expired' 
                ORDER BY endDate DESC LIMIT 1
            """
            cursor.execute(sql_select, (user_username,))
            row = cursor.fetchone()
            
        return SubscriptionOut(
            id=row['id'],
            type=row['type'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            status=row['status'],
            user_username=row['user_username']
        )

def has_active_subscription(user_username: str, family: str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "SELECT COUNT(*) as count FROM SUBSCRIPTION WHERE userUsername = ? AND status IN ('active', 'pending')"
            cursor.execute(sql, (user_username,))
            row = cursor.fetchone()
            return row['count'] > 0

def update_subscription_query(user_username: str, new_type: str, end_date: date) -> SubscriptionOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = "UPDATE SUBSCRIPTION SET endDate = ?, type = ?, status = 'active' WHERE userUsername = ? AND status = 'pending'"
            cursor.execute(sql, (end_date, new_type, user_username))
            conn.commit()

            sql_select = """
                SELECT 
                    id, 
                    type, 
                    startDate AS start_date, 
                    endDate AS end_date, 
                    status, 
                    userUsername AS user_username 
                FROM SUBSCRIPTION 
                WHERE userUsername = ? AND status = 'active' 
                ORDER BY endDate DESC LIMIT 1
            """
            cursor.execute(sql_select, (user_username,))
            row = cursor.fetchone()
            
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You don't have an active subscription"
                )
        return SubscriptionOut(
            id=row['id'],
            type=row['type'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            status=row['status'],
            user_username=row['user_username']
        )
# ---------------------------- PROFILE ----------------------------------
def create_profile_query(user_username: str, name: str, color: str) -> dict:
    profile_id = str(uuid.uuid4())
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_select = "SELECT 1 FROM SUBSCRIPTION WHERE userUsername = ? AND status = 'active'"
            cursor.execute(sql_select, (user_username,))
            if not cursor.fetchone():
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
                
            sql_exists = "SELECT 1 FROM PROFILE WHERE userUsername = ? AND name = ?"
            cursor.execute(sql_exists, (user_username, name))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This profile already exists"
                )

            sql_insert = "INSERT INTO PROFILE (id, userUsername, name, profileColor) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_insert, (profile_id, user_username, name, color))
            conn.commit()

            return {
                "id": profile_id,
                "user_username": user_username,
                "name": name,
                "profile_color": color
            }

def delete_profile_query(user_username: str, name: str) -> dict:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_exists = "SELECT id FROM PROFILE WHERE userUsername = ? AND name = ?"
            cursor.execute(sql_exists, (user_username, name))
            row = cursor.fetchone()

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This profile doesnt exist"
                )

            profile_real_id = row[0]

            sql_history = "DELETE FROM HISTORY WHERE profileId = ?"
            cursor.execute(sql_history, (profile_real_id,))
            
            sql_delete = "DELETE FROM PROFILE WHERE userUsername = ? AND name = ?"
            cursor.execute(sql_delete, (user_username, name))
            
            conn.commit()
            return {"name": name}

def update_full_profile_query(profile_id: str, new_name: str, new_color: str) -> dict:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            try:
                sql_update = """
                    UPDATE PROFILE 
                    SET name = ?, profileColor = ? 
                    WHERE id = ?
                """
                cursor.execute(sql_update, (new_name, new_color, profile_id))
                
                sql_select = """
                    SELECT id, userUsername, name, profileColor 
                    FROM PROFILE 
                    WHERE id = ?
                """
                cursor.execute(sql_select, (profile_id,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                conn.commit()

                # Mapeo manual
                return {
                    "id": row[0],
                    "user_username": row[1],
                    "name": row[2],
                    "profile_color": row[3]
                }
                
            except mariadb.IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Profile name already exists"
                )
            
def get_profiles_query(user_username: str) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Mapeo estricto de columnas camelCase a los atributos de ProfileOut (profile_color)
            sql = """
                SELECT 
                    id, 
                    userUsername AS user_username, 
                    name, 
                    profileColor AS profile_color 
                FROM PROFILE 
                WHERE userUsername = ?
            """
            cursor.execute(sql, (user_username,))
            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "user_username": row[1],
                    "name": row[2],
                    "profile_color": row[3]
                }
                for row in rows
            ]

# ------------ PAYMENTS -----------------
def confirm_payment_query(user_username: str, method: PaymentType, subscription_id: str) -> PaymentOut:
    payment_date = date.today()

    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:

            sql_select = """
                         SELECT id, type, status
                         FROM SUBSCRIPTION
                         WHERE id = ? AND userUsername = ?
                         """
            cursor.execute(sql_select, (subscription_id, user_username))
            row = cursor.fetchone()

            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription not found for this user"
                )

            sub_id, sub_type, sub_status = row

            if sub_status == "active":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This subscription is already active"
                )

            if sub_status == "expired":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This subscription has already expired"
                )

            price_map = {
                "standard": 9.99,
                "standard_yearly": 99.99,
                "premium": 14.59,
                "premium_yearly": 140.59
            }

            if sub_type not in price_map:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid subscription type: {sub_type}"
                )

            amount = price_map[sub_type]
            payment_id = str(uuid.uuid4())

            sql_insert = """
                         INSERT INTO PAYMENT
                             (id, subscriptionId, paymentDate, method, amount)
                         VALUES (?, ?, ?, ?, ?)
                         """
            cursor.execute(sql_insert, (payment_id, sub_id, payment_date, method, amount))

            sql_update = "UPDATE SUBSCRIPTION SET status = 'active' WHERE id = ?"
            cursor.execute(sql_update, (sub_id,))

            conn.commit()

    return PaymentOut(
        id=payment_id,
        subscription_id=sub_id,
        payment_date=payment_date,
        method=method,
        status="completed",
        amount=amount
    )

def get_payments_query(user_username) -> list:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
                  SELECT p.id, p.subscriptionId, p.paymentDate, p.method, p.status, p.amount
                  FROM PAYMENT p
                           JOIN SUBSCRIPTION s ON p.subscriptionId = s.id
                  WHERE s.userUsername = ? \
                  """
            cursor.execute(sql, (user_username,))
            rows = cursor.fetchall()
        return [
            PaymentOut(
                id=row['id'],
                subscription_id=row['subscriptionId'],
                payment_date=row['paymentDate'],
                method=row['method'],
                status=row['status'],
                amount=row['amount']
            )
            for row in rows
        ]
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
                      id,
                      title,
                      description,
                      duration,
                      ageRating    AS age_rating,
                      coverUrl     AS cover_url,
                      videoUrl     AS video_url,
                      type,
                      logoUrl      AS logo_url,
                      portraitUrl  AS portrait_url,
                      uploadDate   AS upload_date,
                      releaseDate  AS release_date
                  FROM CONTENT
                  """
            cursor.execute(sql)
            return cursor.fetchall()


def get_content_by_title_query(title: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = sql = """
                        SELECT title, description, duration, ageRating, coverUrl, videoUrl, type, uploadDate, releaseDate, logoUrl, portraitUrl
                        FROM CONTENT
                        WHERE title = ?"""
            values = (title,)
            cursor.execute(sql, values)

            row = cursor.fetchone()
            if row:
                return ContentUser(title=row[0], description=row[1], duration=row[2],
                                   age_rating=row[3], cover_url=row[4], video_url=row[5],
                                   type=row[6], upload_date=row[7], release_date=row[8],
                                   logo_url=row[9], portrait_url=row[10])
            return None


def create_content_query(content: ContentDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            uploadDate = date.today()
            sql = "INSERT INTO CONTENT (id, title, description, duration, ageRating, coverUrl, videoUrl, type, logoUrl, portraitUrl, uploadDate, releaseDate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
            values = (content.id, content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type, content.logo_url, content.portrait_url, uploadDate, content.release_date)
            cursor.execute(sql, values)
            conn.commit()


def modify_content_query(content: ContentUser, id_content: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTENT SET title=?, description=?, duration=?, ageRating=?, coverUrl=?, videoUrl=?, type=?, logoUrl=?, portraitUrl=?, releaseDate =? WHERE id=?"
            values = (content.title, content.description, content.duration, content.age_rating, content.cover_url, content.video_url, content.type, content.logo_url,content.portrait_url, content.release_date, id_content)
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
        
def get_content_by_genre_query(genre_name: str) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
                SELECT 
                    c.id, 
                    c.title, 
                    c.description, 
                    c.duration, 
                    c.ageRating AS age_rating, 
                    c.coverUrl AS cover_url, 
                    c.videoUrl AS video_url, 
                    c.type, 
                    c.logoURL AS logo_url, 
                    c.portraitURL AS portrait_url, 
                    c.uploadDate AS upload_date, 
                    c.releaseDate AS release_date
                FROM CONTENT c
                INNER JOIN CONTENT_GENRE cg ON c.id = cg.contentId
                INNER JOIN GENRE g ON cg.genreId = g.id
                WHERE LOWER(g.name) = LOWER(?);
            """
            cursor.execute(sql, (genre_name,))
            return cursor.fetchall()
# ---------------------- GENRE ----------------------
def get_all_genres_query():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary = True) as cursor:
            sql = "SELECT id, name FROM GENRE"
            cursor.execute(sql)
            row = cursor.fetchall()
            if not row:
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
            

def assign_genre_to_content_query(content_id: str, genre_id: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Validar si el contenido existe
            cursor.execute("SELECT id FROM CONTENT WHERE id = ?", (content_id,))
            if not cursor.fetchone():
                raise HTTPException(404, "Content not found")

            # Validar si el género existe
            cursor.execute("SELECT id FROM GENRE WHERE id = ?", (genre_id,))
            if not cursor.fetchone():
                raise HTTPException(404, "Genre not found")

            # Validar si ya están relacionados (para no duplicar)
            sql_check = "SELECT 1 FROM CONTENT_GENRE WHERE contentId = ? AND genreId = ?"
            cursor.execute(sql_check, (content_id, genre_id))
            if cursor.fetchone():
                raise HTTPException(400, "This content already has this genre assigned")

            # Hacer la inserción si todo está correcto
            sql_insert = "INSERT INTO CONTENT_GENRE (contentId, genreId) VALUES (?, ?)"
            cursor.execute(sql_insert, (content_id, genre_id))
            conn.commit()  # ¡No olvides el commit para guardar los cambios!


def remove_genre_from_content_query(content_id: str, genre_id: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Validar si la relación realmente existe antes de borrar
            sql_check = "SELECT 1 FROM CONTENT_GENRE WHERE contentId = ? AND genreId = ?"
            cursor.execute(sql_check, (content_id, genre_id))
            if not cursor.fetchone():
                raise HTTPException(404, "The relation between this content and genre does not exist")

            # Eliminar la relación
            sql_delete = "DELETE FROM CONTENT_GENRE WHERE contentId = ? AND genreId = ?"
            cursor.execute(sql_delete, (content_id, genre_id))
            conn.commit()

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
    semanas_atras = 2
    limite_semanas = 52
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            while semanas_atras <= limite_semanas:
                hoy = date.today()
                fecha_inicio = hoy - timedelta(weeks=semanas_atras)
                sql_select = """
                             SELECT title, description, duration,
                                    ageRating AS age_rating, coverUrl AS cover_url,
                                    videoUrl AS video_url, type,
                                    logoUrl AS logo_url, portraitUrl AS portrait_url,
                                    uploadDate AS upload_date, releaseDate AS release_date
                             FROM CONTENT
                             WHERE uploadDate BETWEEN ? AND ?
                             ORDER BY uploadDate DESC LIMIT 10 \
                             """
                cursor.execute(sql_select, (fecha_inicio, hoy))
                resultados = cursor.fetchall()
                if resultados:
                    return resultados
                semanas_atras += 2
    return []
# ---------------------- EPISODES ----------------------
def get_episodes_by_content_query(content_id: str) -> list:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor(dictionary=True) as cursor:
            sql_check = "SELECT 1 FROM CONTENT WHERE id = ?"
            cursor.execute(sql_check, (content_id,))
            if not cursor.fetchone():
                raise HTTPException(404, f"Content '{content_id}' not found")

            sql = """
                  SELECT id, contentId AS content_id, season, episode,
                         title, description, duration,
                         videoUrl AS video_url, coverUrl AS cover_url
                  FROM EPISODE
                  WHERE contentId = ?
                  ORDER BY season, episode
                  """
            cursor.execute(sql, (content_id,))
            return cursor.fetchall()

def create_episode_query(ep: EpisodeDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_check = "SELECT 1 FROM CONTENT WHERE id = ? AND type = 'series'"
            cursor.execute(sql_check, (ep.content_id,))
            if not cursor.fetchone():
                raise HTTPException(400, "Content not found or is not a series")

            sql_dup = """
                      SELECT 1 FROM EPISODE
                      WHERE contentId = ? AND season = ? AND episode = ?
                      """
            cursor.execute(sql_dup, (ep.content_id, ep.season, ep.episode))
            if cursor.fetchone():
                raise HTTPException(409, f"Episode S{ep.season}E{ep.episode} already exists")

            sql = """
                  INSERT INTO EPISODE
                  (id, contentId, season, episode, title, description, duration, videoUrl, coverUrl)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """
            cursor.execute(sql, (
                ep.id, ep.content_id, ep.season, ep.episode,
                ep.title, ep.description, ep.duration,
                ep.video_url, ep.cover_url
            ))
            conn.commit()

def delete_episode_query(episode_id: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_check = "SELECT 1 FROM EPISODE WHERE id = ?"
            cursor.execute(sql_check, (episode_id,))
            if not cursor.fetchone():
                raise HTTPException(404, "Episode not found")

            cursor.execute("DELETE FROM EPISODE WHERE id = ?", (episode_id,))
            conn.commit()
            return {"deleted_episode_id": episode_id}

def update_episode_query(episode_id: str, ep: EpisodeBase):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_check = "SELECT 1 FROM EPISODE WHERE id = ?"
            cursor.execute(sql_check, (episode_id,))
            if not cursor.fetchone():
                raise HTTPException(404, "Episode not found")

            sql = """
                  UPDATE EPISODE
                  SET season=?, episode=?, title=?, description=?,
                      duration=?, videoUrl=?, coverUrl=?
                  WHERE id=?
                  """
            cursor.execute(sql, (
                ep.season, ep.episode, ep.title, ep.description,
                ep.duration, ep.video_url, ep.cover_url, episode_id
            ))
            conn.commit()
            return {"updated_episode_id": episode_id}