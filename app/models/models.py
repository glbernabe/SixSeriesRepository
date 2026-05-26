from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date, timedelta, datetime, time
from pydantic.alias_generators import to_camel
from enum import Enum
from typing import Optional

class UserRolEnum(str, Enum):
    USER = "user"
    SUPERUSER = "superuser"

class RefreshRequest(BaseModel):
    refresh_token: str

class PermissionsUserEnum(str, Enum):
    TOTAL = "total"
    CREATE = "create"
    EDIT = "edit"
    READ = "read"
    NONE = "none"

class SubscriptionCatalog(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"
    STANDARD_YEARLY = "standard_yearly"
    PREMIUM_YEARLY = "premium_yearly"


class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"

class SubscriptionRequest(BaseModel):
    type: str

class RatingValue(str, Enum): pass

# -------------------- User Models --------------------
class UserBase(BaseModel):
    username: str
    email: str
    rol: UserRolEnum = UserRolEnum.USER
    permissions: PermissionsUserEnum = PermissionsUserEnum.NONE

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
    type: SubscriptionCatalog


class SubscriptionRequest(SubscriptionBase):
    pass


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionDb(SubscriptionCreate):
    id: str
    user_username: str
    start_date: date
    end_date: date
    status: SubscriptionStatus


class SubscriptionOut(SubscriptionBase):
    id: str
    user_username: str
    start_date: date
    end_date: date
    status: SubscriptionStatus

# -------------------- Payment Models --------------------
class PaymentCreate(BaseModel):
    method: str
    amount: float

class PaymentDb(BaseModel):
    id: str
    subscription_id: str
    payment_date: date
    method: str
    status: str
    amount: float

class PaymentType(str, Enum):
    PAYPAL = "paypal"
    CARD = "card"

class PaymentOut(BaseModel):
    id: str
    subscription_id: str
    payment_date: date
    method: PaymentType
    status: str
    amount: float

class PaymentRequest(BaseModel):
    subscription_id: str
    method: PaymentType
    amount: float
# -------------------- Profile Models --------------------
class ProfileDb(BaseModel):
    id: str
    user_id: str
    name: str
    profile_color: str | None = None

class ProfileCreateRequest(BaseModel):
    name: str
    color: str = "#6A6A69"

class ProfileOut(BaseModel):
    id: str
    user_username: str
    name: str
    profile_color: str | None = None
    
# -------------------- Content Models --------------------
class ContentType(str, Enum):
    SERIES = "series"
    MOVIE = "movie"
    DOCUMENTARY = "documentary"

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
    upload_date: Optional[date]
    release_date: Optional[date] = None

class ContentDb(ContentUser):
    id: str

# -------------------- Gender Models --------------------

class Genre(BaseModel):
    id: str
    name: str


class RatingValue(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    UNRATED = "unrated"

class RatingCreate(BaseModel):
    content_title: str
    rating: RatingValue

class RatingOut(BaseModel):
    title: str
    rating: RatingValue



class HistoryCreate(BaseModel):
    content_title: str
    time_viewed: int

class HistoryOut(BaseModel):
    title: str
    last_watched: datetime
    time_viewed: int