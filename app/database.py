from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from .config import settings

#SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{urlquote('Aerospace@1')}@localhost:5432/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{urlquote(settings.database_password)}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='Aerospace@1', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
