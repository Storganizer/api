from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite+pysqlite:///storganizer.db", echo=True)

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

#session = Session(engine)
