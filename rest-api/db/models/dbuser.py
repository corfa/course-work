from sqlalchemy import Column, Integer, String, BOOLEAN,ForeignKey
from sqlalchemy.orm import relationship

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

class DBFiles(BaseModel):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("DBUsers", back_populates="files")

DBUsers.files = relationship("DBFiles", back_populates="owner")