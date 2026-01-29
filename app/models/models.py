from pydantic import BaseModel
from datetime import date
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

class UserId(BaseModel):
    id: str

class UserDb(BaseModel):
    id: str
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: str | None = None
    username: str
    email: str

class SubscriptionBase(BaseModel):
    type: str
class SubscriptionCreate(SubscriptionBase):
    pass
class SubscriptionDb(SubscriptionCreate):
    id: str
    user_username: str
    startdate: date
    endDate: date
    status: str
    type: str

class SubscriptionOut(BaseModel):
    type: str
    startDate: date
    endDate: date
    status: str
class PaymentCreate(BaseModel):
    method: str
    amount: float

class PaymentDb(BaseModel):
    id: str
    subscription_id: str
    paymentDate: date
    method: str
    status: str
    amount: float

class PaymentOut(BaseModel):
    paymentDate: date
    method: str
    amount: float

class ProfileDb(BaseModel):
    id: str
    user_id: str
    name: str

class ProfileOut(BaseModel):
    name: str
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


