from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///storganizer.db", echo=True)
session = Session(engine)