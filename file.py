from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base 
import PIL.Image,io
import werkzeug,base64
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields, reqparse

app = Flask(__name__)
api = Api(app)
file_upload = reqparse.RequestParser()
file_upload.add_argument('file 1',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='file')
file_upload.add_argument('file 2',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='file')
app.config['SWAGGER_UI_JSONEDITOR'] = True
db =  create_engine('postgresql+pg8000://root:root@localhost/demo')  
base = declarative_base()

class Image(base):  
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    file1 = Column(String, nullable = False)
    file2 = Column(String, nullable = False)


Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)


@api.route('/postfile')
class postfile(Resource):
    @api.expect(file_upload)
    def post(self):
        f = request.files['file 1']
        f1 = request.files['file 2']  
        f.save(f.filename)
        f1.save(f1.filename)
        new = Image(file1=f.filename,file2=f1.filename)
        session.add(new)
        session.commit()
        return jsonify({"msg":"stored successfully"})  

@api.route('/displayfile1/<int:id>')
class displayfile(Resource): 
    def get(self,id):
       image = session.query(Image).filter(Image.id==id).one()
       file1 = image.file1
       return send_file(file1)

@api.route('/displayfile2/<int:id>')
class displayfile(Resource): 
    def get(self,id):
       image = session.query(Image).filter(Image.id==id).one()
       file2 = image.file2
       return send_file(file2)


if __name__ == '__main__':
    app.run(debug=True)

