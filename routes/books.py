from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.responses import Response,JSONResponse
from db import Session,get_db
from db_models.book import Book
from models.bookmodel import *
import json

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
def get_all_books(offset:int=0,limit:int=10,name:str="",db:Session=Depends(get_db)):
    books=db.query(Book).filter(Book.name.ilike(f"%{name}%")).offset(offset).limit(limit).all()
    return books

@router.get("/recent",response_model=list[allInfo])
def get_recent_book(offset:int=0,limit:int=10,db:Session=Depends(get_db)):
    books=db.query(Book).order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return books
