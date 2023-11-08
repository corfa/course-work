from sqlalchemy import Column, Integer, String, BOOLEAN

from db.models.base import BaseModel


class DBUsers(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String,unique=True)
    email = Column(String,unique=True)
    token = Column(String,unique=True)
    confirmed = Column(BOOLEAN,default=False)
    is_delete = Column(BOOLEAN,default=False)

