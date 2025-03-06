from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.responses import Response,JSONResponse
from models.usermodel import getByToken,register
from db import Session,get_db
from db_models.user import User
from utils.security import decode_token
import bcrypt


import json

router = APIRouter()

@router.get("/getByToken", response_model=getByToken,description="Nota: Requiere un jwt Bearer token para asi poder devolver los datos del usuario.")
def get_profile_by_email(db:Session=Depends(get_db),dependencies=Depends(decode_token)):
    try:
        user=db.query(User).filter_by(email=dependencies["email"]).first()
        print(user)
    except:
        raise HTTPException(status_code=400, description="el token recibido no es valido")
    return user

@router.put("/update")
def update_profile(data:register, db:Session=Depends(get_db),dependencies=Depends(decode_token)):
    user=db.query(User).filter_by(email=dependencies["email"]).first()
    if user!=None:
        hashed_password=bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())
        user.username=data.username
        user.email=data.email
        user.password=hashed_password.decode("utf-8")
        db.commit()
        db.refresh(user)
        return JSONResponse({},status_code=200)
    return HTTPException(status_code=400,detail="No se ha encontrado el usuario")

