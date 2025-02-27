from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey  #Para creacion de modelos


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id=Column(Integer, ForeignKey("roles.rol_id"))
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    
    def __init__(self,rol_id,username,email,password):
        self.rol_id=rol_id
        self.username=username
        self.email=email
        self.password=password
