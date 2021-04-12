from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base  
from datetime import datetime


base = declarative_base()

class Repo(base):  
    __tablename__ = 'repo_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(String, nullable = False)
    User = Column(String, nullable = False)
    Level = Column(String, nullable = False)
    Message = Column(String, nullable = False)



def create(date,user,level,message):
  db =  create_engine('postgresql+pg8000://root:root@localhost/demo')  
  Session = sessionmaker(db)  
  session = Session()
  base.metadata.create_all(db)
  for i in range(len(user)):
	  new1 = Repo(Date=date[i],User=user[i],Level=level[i],Message=message[i])
	  try:
	  	session.add(new1)
	  	session.commit()
	  	print("stored successfully")
	  except Exception as e:
	  	session.rollback()
	  	print(e)

def read():
	with open("repo.log") as file_in:
	    a = file_in.read()
	    x = a.split("#")
	    

	Date = 0
	date = []
	User = 1
	user = []
	Level = 2
	level = []
	Message = 3
	message = []
	for i in range(len(x)):
		if i==Date+4:
			date.append(x[i])
			Date = Date+4
		elif i==User or i==User+4:
			user.append(x[i])
			User = User+4
		elif i==Level or i==Level+4:
			level.append(x[i])
			Level = Level+4
		elif i==Message or i==Message+4:
			message.append(x[i])
			Message = Message+4
	return date,user,level,message
        	

date,user,level,message = read()
print(date)
print(user)
print(level)
print(message)
create(date,user,level,message)









    
    
