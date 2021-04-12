from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base  



app = Flask(__name__)
db =  create_engine('mssql+pymssql://SA:Mauvais@1234@localhost/demo')  
base = declarative_base()

class Employee(base):  
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    details = relationship('Details',backref='employee')

class Details(base):
    __tablename__= 'details'

    id = Column(Integer , primary_key=True)
    Designation = Column(String , nullable = False)
    Contact = Column(String ,nullable = False)
    Employee_id = Column(Integer,ForeignKey('employee.id'))

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

@app.route('/addEmployee' ,methods=['POST'])
def save():
    data = request.json
    name = data['name']
    id = data['id']
    designation = data['designation']
    contact = data['contact']
    new = Employee(id=id,name =name)
    new1 = Details(id=id,Designation=designation,Contact=contact,Employee_id=id)
    try:
        session.add(new)
        session.add(new1)
        session.commit()
        return jsonify({"msg":"stored successfully"})
    except Exception as e:
        session.rollback()
        print(e)

@app.route('/getallEmployee',methods=['GET'])
def getAll():
    try:
        details = session.query(Details).all()
        result = list()
        for detail in details:
            employee = session.query(Employee).filter(Employee.id == detail.Employee_id).one()
            result_dict = {"id":detail.id,"name":employee.name,"Designation":detail.Designation,"Contact":detail.Contact}
            result.append(result_dict)
        session.commit()
        return json.dumps(result)
    except Exception as e:
        session.rollback()
        print(e)

@app.route('/getemployeebyId/<int:id>',methods=['GET'])
def getbyId(id):
    try:
        details = session.query(Details).filter(Details.id == id).all()
        result = list()
        for detail in details:
            employee = session.query(Employee).filter(Employee.id == detail.Employee_id).one()
            result_dict = {"id":detail.id,"name":employee.name,"Designation":detail.Designation,"Contact":detail.Contact}
            result.append(result_dict)
        session.commit()
        print(result)
        return json.dumps(result)
    except Exception as e:
        session.rollback()
        print(e)

@app.route('/updateemployee',methods=['put'])
def update():
    try:
        data = request.json
        id = data['id']
        name = data['name']
        Designation = data['designation']
        Contact = data['contact']
        employee = session.query(Employee).filter(Employee.id == id).one()
        detail = session.query(Details).filter(Details.id == id).one()
        employee.name = name
        detail.Designation = Designation
        detail.Contact = Contact
        session.commit()
        return jsonify({"msg":"successfully updated"})
    except Exception as e:
        session.rollback()
        print(e)

@app.route('/deleteemployee/<int:id>',methods=['DELETE'])
def delete(id):
    try:
        employee = session.query(Employee).filter(Employee.id == id).one()
        detail = session.query(Details).filter(Details.id == id).one()
        session.delete(employee)
        session.delete(detail)
        session.commit()
        return jsonify({"msg":"Deleted"})
    except Exception as e:
        session.rollback()
        print(e)
        
    
if __name__ == '__main__':
    app.run(debug=True)
