from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from models.usermodel import *
from db import Session,get_db
from db_models.user import User
import bcrypt

router = APIRouter()

@router.post("/register")
def register_user(user:register, db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password=bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user=User(user.username,user.email,hashed_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return JSONResponse({},status_code=201)


@router.post("/login")
def login_user(user: login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    return {"message": "Inicio de sesión exitoso"}