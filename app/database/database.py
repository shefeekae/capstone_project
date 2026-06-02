from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:4268@localhost:5432/capestone"
engine = create_engine(db_url)
 
session = sessionmaker(autocommit = False,autoflush= False, bind=engine)