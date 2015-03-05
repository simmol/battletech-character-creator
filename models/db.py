from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///battletech-character-creator.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
