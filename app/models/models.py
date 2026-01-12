from pydantic import BaseModel
from enum import Enum

class UserBase(BaseModel):
    email: str

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

class ContentType(str, Enum):
    series = "series"
    movie = "movie"
    documentary = "documentary"

class Content(BaseModel):
    id: str | None = None
    title: str
    description: str
    duration: int
    age_rating: str
    cover_url: str
    video_url: str
    type: ContentType

