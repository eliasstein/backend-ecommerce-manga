from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import Response,JSONResponse
from models import usermodel
import json

router = APIRouter()

@router.post("/register")
def read_root(user_register:usermodel.register):

    return Response(status_code=201)


@router.post("/login")
def read_root(user_login:usermodel.login):

    return JSONResponse(content={},status_code=200)
