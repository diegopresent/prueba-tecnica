from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import products, categories, images 

Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:5173", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes") # disponible en http://localhost:8000/imagenes/nombreImagen


app.include_router(products.router)
app.include_router(categories.router) 
app.include_router(images.router) 