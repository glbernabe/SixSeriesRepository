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
    id: str
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: str | None = None
    username: str
    email: str
