from pydantic import BaseModel,EmailStr,StrictBool

class register(BaseModel):
    username:str
    email:EmailStr
    password:str

class login(BaseModel):
    email:EmailStr
    password:str
    remember:bool

class getByToken(BaseModel):
    username:str
    email:EmailStr
