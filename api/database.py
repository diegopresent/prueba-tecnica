import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene las variables de entorno para la conexión a la base de datos
db_username = os.getenv("USER_DB")
db_password = os.getenv("PASSWORD_DB")
db_host = os.getenv("HOST_DB")
db_port = os.getenv("PORT_DB")
db_name = os.getenv("DATABASE_NAME")

# Construye la URL de conexión a la base de datos MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Crea el motor de SQLAlchemy para la conexión a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base para los modelos de la base de datos SQLAlchemy
# Esta clase se utilizará para definir las tablas y sus relaciones
Base = declarative_base()

# Función para obtener una sesión de base de datos como dependencia en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()