from db import Base
from sqlalchemy import Column, Integer, String  #Para creacion de modelos


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}',email='{self.email},password='{self.password}')"
    
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
