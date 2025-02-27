from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import JSONResponse
from models.usermodel import *
from db import Session,get_db
from db_models.user import User
from utils.security import Security
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
    
    return {"message": "Inicio de sesión exitoso",
            "access_token":Security.generate_token({"email":user.email},0,1, False),
            "refresh_token":Security.generate_token({"email":user.email},0,30, True)
            }

#Ejemplo de como validar el token
@router.get('/verify')
def verifyToken(request:Request):
    #Almacenamos los datos del token o el error si existe
    token=Security.verify_token(request.headers, False)
    #Comprobamos si es un token valido
    if token["success"]==False:
        return token
    #Si es True continuamos con el codigo
    #Si la ip existe en el diccionario de intentos entonces la borramos
    return {"test":"test"}