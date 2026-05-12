from pydantic import BaseModel, field_validator
from datetime import date, time, timedelta
from enum import Enum
from typing import Optional

class UserRolEnum(str, Enum):
    user = "user"
    superuser = "superuser"

class PermissionsUserEnum(str, Enum):
    total = "total"
    create = "create"
    edit = "edit"
    read = "read"
    none = "none"
    
# -------------------- User Models --------------------
class UserBase(BaseModel):
    username: str
    email: str
    rol: UserRolEnum = UserRolEnum.user
    permissions: PermissionsUserEnum = PermissionsUserEnum.none

class UserId(BaseModel):
    id: str

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserDb(UserBase):
    id: str
    password: str

class UserOut(UserBase):
    id: str
    
# -------------------- Subscription Models --------------------
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

# -------------------- Payment Models --------------------
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

# -------------------- Profile Models --------------------
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
    duration: time
    age_rating: str
    cover_url: str | None = None # La imagen del carusel en grande
    video_url: str
    type: ContentType
    logo_url: str | None = None # La imagen del logo en el carusel
    portrait_url: str | None = None # La imagen que siempre tiene que tener

    #MariaDB hace llegar un 'timedelta' y entonces antes de llegar, lo pasamos a 'time' HH:MM:SS
    @field_validator("duration", mode="before")
    @classmethod
    def parse_duration(cls, v):
        if isinstance(v, timedelta):
            total_seconds = int(v.total_seconds())
            hours = (total_seconds // 3600) % 24 
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return time(hour=hours, minute=minutes, second=seconds)
        return v

class ContentDb(ContentUser):
    id: str

# -------------------- Gender Models --------------------

class Genre(BaseModel):
    id: str
    name: str


