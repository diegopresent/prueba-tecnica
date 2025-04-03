from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import products, categories, images

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI

app = FastAPI()
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/imagenes", StaticFiles(directory="imagenes"), name="imagenes")

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(images.router)