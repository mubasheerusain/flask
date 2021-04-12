from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base  
from datetime import datetime


base = declarative_base()

class Software(base):  
    __tablename__ = 'software_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    log = Column(String, nullable = False)
    time = Column(DateTime, nullable=False)



def create(data):
  db =  create_engine('postgresql+pg8000://root:root@localhost/demo')  
  Session = sessionmaker(db)  
  session = Session()
  base.metadata.create_all(db)
  new1 = Software(log=data,time=datetime.now(tz=None))
  try:
  	session.add(new1)
  	session.commit()
  	print("stored successfully")
  except Exception as e:
  	session.rollback()
  	print(e)

def read():
    f = open("Ping_output20200909161751.log", "r")
    temp=f.read()
    return temp

log = read()
create(log)





