from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.responses import Response,JSONResponse
from sqlalchemy import not_
from db import Session,get_db
from db_models.book import Book
from models.bookmodel import *

router = APIRouter()

@router.post("/register", response_model=allInfo)
def register_book(book:registerBook,db:Session=Depends(get_db)):
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
                  mangas:bool=None,
                  comics:bool=None,
                  stock:bool=None,
                  adult:bool=None, 
                  db:Session=Depends(get_db)):
    books=(db.query(Book).filter(Book.name.ilike(f"%{name}%"))
    .filter(Book.type.ilike("%Manga%") if mangas else Book.type.ilike("%%"))
    .filter(Book.type.ilike("%Comic%") if comics else Book.type.ilike("%%")))
    
    if stock is not None:
        books=books.filter(Book.quantity>0 if stock else Book.quantity<1)
    if adult is not None:
        books=books.filter(Book.adult==adult)
    books=books.offset(offset).limit(limit).all()
    return books

@router.get("/recent",response_model=list[allInfo])
def get_recent_book(offset:int=0,limit:int=10,db:Session=Depends(get_db)):
    books=db.query(Book).order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return books
