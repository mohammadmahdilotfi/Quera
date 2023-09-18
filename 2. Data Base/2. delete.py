from typing import List,Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

DB_NAME = 'Transfermarkt_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="1234",
    host="localhost",
    database=DB_NAME

)


# engine = create_engine(url_object)


def create_database():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))


def show_database():
    with engine.connect() as conn:
        results = conn.execute(text('SHOW DATABASES;'))
        for res in results:
            return res


engine = create_engine(url_object)
create_database()