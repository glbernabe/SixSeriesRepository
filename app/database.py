import mariadb
from app.models.models import UserDb, ContentDb, ContentUser, Genre
from fastapi import HTTPException

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
        with conn.cursor() as cursor:
            sql = "SELECT * FROM `CONTENT`"
            cursor.execute(sql)
            rows = cursor.fetchall()

            titles = []
            for row in rows:
                titles.append(row)
            return titles


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
            rows = cursor.fetchall()

            if cursor.rowcount == 0:
                raise HTTPException(404, "There are no genres")
            conn.commit()
            return rows
        
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

