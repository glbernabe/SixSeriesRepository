from pydantic import BaseModel
from enum import Enum
from typing import Optional

# -------------------- User Models --------------------

class UserBase(BaseModel):
    email: str

class UserId(BaseModel):
    id: str

class UserRegister(UserBase):
    username: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserDb(BaseModel):
    id: str
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: str | None = None
    username: str
    email: str

# -------------------- Content Models --------------------
class ContentType(str, Enum):
    series = "series"
    movie = "movie"
    documentary = "documentary"

class ContentUser(BaseModel):    
    title: str
    description: str
    duration: int
    age_rating: str
    cover_url: str
    video_url: str
    type: ContentType

class ContentDb(ContentUser):
    id: str

# -------------------- Gender Models --------------------

class Genre(BaseModel):
    id: str
    name: str
