from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.responses import Response,JSONResponse
from sqlalchemy import not_
from db import Session,get_db
from utils.security import decode_token
from db_models.book import Book
from models.bookmodel import *

router = APIRouter()

@router.post("/register", response_model=allInfo, description="Nota: Requiere de un Access token enviado como Bearer token en el encabezado con el rol de administrador para poder ser utilizado")
def register_book(book:registerBook,db:Session=Depends(get_db), dependencies=Depends(decode_token)):
    if dependencies["rol"]!=1:
        raise HTTPException(status_code=401, detail="El usuario no es administrador")
    
    db_book=Book(book.type,
                 book.name,
                 book.description,
                 book.price,
                 book.image,
                 book.genre,
                 book.adult,
                 book.quantity)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/all",response_model=list[allInfo])
def get_all_books(offset:int=0,limit:int=10,db:Session=Depends(get_db)):
    books=db.query(Book).offset(offset).limit(limit).all()
    return books

@router.get("/getByName",response_model=list[allInfo])
def get_all_books(offset:int=0, 
                  limit:int=10,
                  name:str="",
                  type:str=None,
                  stock:bool=None,
                  adult:bool=None, 
                  db:Session=Depends(get_db)):
    books=(db.query(Book).filter(Book.name.ilike(f"%{name}%"))
    .filter(Book.type.ilike(f"%{type}%") if type else Book.type.ilike("%%")))
    if stock is not None:
        books=books.filter(Book.quantity>0 if stock else Book.quantity<1)
    if adult is not None:
        books=books.filter(Book.adult==adult)
    books=books.offset(offset).limit(limit).all()
    return books

@router.get("/getById",response_model=allInfo)
def get_all_books(id:int=0,db:Session=Depends(get_db)):
    book=db.query(Book).get(id)
    return book



@router.get("/recent",response_model=list[allInfo])
def get_recent_book(offset:int=0,limit:int=10,db:Session=Depends(get_db)):
    books=db.query(Book).order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return books