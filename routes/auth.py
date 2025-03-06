from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import JSONResponse
from models.usermodel import *
from db import Session,get_db
from db_models.user import User
from utils.security import Security
import bcrypt
from datetime import datetime,timedelta

router = APIRouter()

@router.post("/register")
def register_user(user:register, db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password=bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user=User(2,user.username,user.email,hashed_password.decode("utf-8"))
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
    if user.remember:
        return {"message": "Inicio de sesión exitoso",
                "access_token":f"access_token={Security.generate_token(
                    {"email":user.email,
                     "rol":db_user.rol_id},0,1, False)};Max-Age=86400; path=/",
                "refresh_token":f"refresh_token={Security.generate_token({"email":user.email,
                                                                          "rol":db_user.rol_id},0,30, True)}; path=/"
                }
    
    #Si no tiene el boton de remember activado entonces retornamos un Access_token simple
    return {"message": "Inicio de sesión exitoso",
            "access_token":f"access_token={Security.generate_token(
                {"email":user.email,
                    "rol":db_user.rol_id},0,1, False)};Max-Age=86400; path=/",
            }

#Ejemplo de como validar el token
@router.get('/verify',
            description="Verifica el token que se envia en el header (Authorization) y devuelve si es valido o no")

def verifyToken(request:Request):
    #Almacenamos los datos del token o el error si existe
    token=Security.verify_token(request.headers, False)
    #Comprobamos si es un token valido
    if token["success"]==False:
        return token
    #Si es True continuamos con el codigo
    #Si la ip existe en el diccionario de intentos entonces la borramos
    return {"message":f"Token verificado con exito","token":token}

@router.get("/refresh")
def refreshToken(request:Request):
    token=Security.refresh_token(request.headers)
    if token["success"]==False:
        return token
    return {"message":f"Token refrescado con exito","token":token}
