from db import Base
from sqlalchemy import Column, Integer, String,Float,Boolean  #Para creacion de modelos


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True,autoincrement=True)
    type=Column(String)
    name = Column(String)
    description= Column(String)
    price = Column(Float)
    image = Column(String)
    genre=Column(String)
    adult=Column(Boolean)
    quantity = Column(Integer)
    
    def __repr__(self):
        return f"{self.id}"
    
    def __init__(self,type,name,description,price,image,genre,adult,quantity):
        self.type=type
        self.name=name
        self.description=description
        self.price=price
        self.image=image
        self.genre=genre
        self.adult=adult
        self.quantity=quantity

    