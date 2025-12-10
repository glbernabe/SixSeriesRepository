from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserRegister(UserBase):
    username: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserDb(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
