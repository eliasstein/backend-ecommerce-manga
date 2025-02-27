from db import Base
from sqlalchemy import Column, Integer, String  #Para creacion de modelos


class Rol(Base):
    __tablename__ = "roles"

    rol_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_name = Column(String)
    rol_description=Column(String)
    
    def __init__(self,rol_name,rol_description):
        self.rol_name=rol_name
        self.rol_description=rol_description
