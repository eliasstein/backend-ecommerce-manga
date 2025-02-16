from db import Base
from sqlalchemy import Column, Integer, String  #Para creacion de modelos


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}',email='{self.email}')"