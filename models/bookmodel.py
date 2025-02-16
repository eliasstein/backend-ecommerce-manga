from pydantic import BaseModel

class allInfo(BaseModel):
    id:int
    type:str
    name:str
    price:float
    image:str
    genre:str
    description:str
    adult:bool
    quantity:int

class registerBook(BaseModel):
    type:str
    name:str
    price:float
    image:str
    genre:str
    description:str
    adult:bool
    quantity:int

class bookInfo(BaseModel):
    name:str
    price:float
    image:str
    description:str
    quantity:int
