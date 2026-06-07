from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date, timedelta, datetime, time
from pydantic.alias_generators import to_camel
from enum import Enum
from typing import Optional, List


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
    ADMIN_LIFE = "admin_life"


class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class SubscriptionRequest(BaseModel):
    type: str


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


# -------------------- Subscription Models --------------------
class SubscriptionBase(BaseModel):
    type: SubscriptionCatalog


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


# -------------------- User Models --------------------
class UserBase(BaseModel):
    username: str
    email: str
    rol: UserRolEnum = UserRolEnum.USER
    permissions: PermissionsUserEnum = PermissionsUserEnum.NONE
    status: bool = True


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
    subscription: Optional[SubscriptionOut] = None
    payment_history: List[PaymentOut] = []


class UserStatusUpdate(BaseModel):
    is_active: bool


# -------------------- Profile Models --------------------
class ProfileDb(BaseModel):
    id: str
    user_username: str
    name: str
    profile_color: str | None = None


class ProfileCreateRequest(BaseModel):
    name: str
    profile_color: str = "#6A6A69"


class ProfileOut(BaseModel):
    id: str
    user_username: str
    name: str
    profile_color: str | None = None


class ProfileUpdateInput(BaseModel):
    name: str
    profile_color: str


# -------------------- Gender Models --------------------
class GenreCreate(BaseModel):
    name: str


class Genre(BaseModel):
    id: str
    name: str


# -------------------- Content Models --------------------
class ContentType(str, Enum):
    SERIES = "series"
    MOVIE = "movie"
    DOCUMENTARY = "documentary"


class ContentUser(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None
    duration: time | None = None
    age_rating: str
    cover_url: str | None = None
    video_url: str | None = None
    type: ContentType
    logo_url: str | None = None
    portrait_url: str | None = None
    upload_date: date | None = None
    release_date: date | None = None
    genres: List[Genre] = []

    @field_validator("duration", mode="before")
    @classmethod
    def parse_duration(cls, v):
        if not v:
            return None
        if isinstance(v, str) and (v.strip() == "" or v == "null"):
            return None
        if isinstance(v, timedelta):
            total_seconds = int(v.total_seconds())
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return time(hour=hours, minute=minutes, second=seconds)
        return v

    @field_validator("upload_date", "release_date", mode="before")
    @classmethod
    def parse_dates(cls, v):
        if isinstance(v, str) and (v.strip() == "" or v == "null"):
            return None
        return v


class ContentDb(ContentUser):
    id: str


# -------------------- Rating Models --------------------
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


# -------------------- History Models --------------------
class HistoryCreate(BaseModel):
    content_title: str
    time_viewed: int


class HistoryOut(BaseModel):
    title: str
    lastWatched: datetime
    timeViewed: int


# -------------------- Episode Models --------------------
class EpisodeBase(BaseModel):
    content_id: str
    season: int = 1
    episode: int
    title: str
    description: Optional[str] = None
    duration: Optional[time] = None
    video_url: str
    cover_url: Optional[str] = None

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


class EpisodeDb(EpisodeBase):
    id: str


class EpisodeOut(EpisodeBase):
    id: str
