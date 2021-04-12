from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base 
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields, reqparse

app = Flask(__name__)
api = Api(app)
file_upload = reqparse.RequestParser()
file_upload.add_argument('file',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='XLS file')
app.config['SWAGGER_UI_JSONEDITOR'] = True
db =  create_engine('postgresql+pg8000://root:root@192.168.43.178/demo')  
base = declarative_base()

class Employee(base):  
    __tablename__ = 'employee_swagger'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)


Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

model = api.model('swagger',{
                   'id':fields.Integer('id'),
                   'name':fields.String('name')})

 
@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        data = request.json
        name = data['name']
        id = data['id']
        new = Employee(id=id,name =name)
        try:
            session.add(new)
            session.commit()
            return jsonify({"msg":"stored successfully"})
        except Exception as e:
            session.rollback()
            print(e)

@api.route('/getAll')
class getAll(Resource):
    def get(self):
        try:
            employees = session.query(Employee).all()
            result = list()
            for employee in employees:
                result_dict = {"id":employee.id,"name":employee.name}
                result.append(result_dict)
            session.commit()
            return jsonify(result)
        except Exception as e:
            session.rollback()
            print(e)  

@api.route('/getbyId/<int:id>')
class getbyId(Resource):
    def get(self,id):
        try:
            employees = session.query(Employee).filter(Employee.id == id).all()
            result = list()
            for employee in employees:
                result_dict = {"id":employee.id,"name":employee.name}
                result.append(result_dict)
            session.commit()
            print(result)
            return jsonify(result)
        except Exception as e:
            session.rollback()
            print(e)  

@api.route('/put')
class update(Resource):
    @api.expect(model)
    def put(self):
        try:
            data = request.json
            id = data['id']
            name = data['name']
            employee = session.query(Employee).filter(Employee.id == id).one()
            employee.name = name
            session.commit()
            return jsonify({"msg":"successfully updated"})
        except Exception as e:
            session.rollback()
            print(e)

@api.route('/delete/<int:id>')
class delete(Resource):
     def delete(self,id):
        try:
            employee = session.query(Employee).filter(Employee.id == id).one()
            session.delete(employee)
            session.commit()
            return jsonify({"msg":"Deleted"})
        except Exception as e:
            session.rollback()
            print(e)

@api.route('/postfile')
class postfile(Resource):
    @api.expect(file_upload)
    def post(self):
        f = request.files['file']  
        f.save(f.filename)
        return jsonify({"msg":"stored successfully"})        

if __name__ == '__main__':
    app.run(debug=True)


