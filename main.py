from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session              #Para cargar la sesion
from db import Base,get_db,engine               #Conexion con la bd
from routes.api import router as api_router

#Importamos los modelos para que se creen en la bd
from db_models.user import User
from db_models.book import Book


app = FastAPI()

origins=["http://localhost",
         "http://localhost:8080",
         "http://localhost:8080",
         "http://localhost:5500",
         "http://localhost:5173",
         "http://127.0.0.1:5500",
         "http://127.0.0.1:5501",
         "https://frontend-ecommerce-manga.vercel.app"
        ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
                   
app.include_router(api_router)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)       #Crea los modelos en la base de datos



@app.get("/",tags=["Hello world"])
def read_root(db:Session=Depends(get_db)):
    # db.query(User).all()
    return {"Hola": "mundo"}


