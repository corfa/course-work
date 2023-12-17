from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str


class UserAuth(BaseModel):
    username: str
    password: str
