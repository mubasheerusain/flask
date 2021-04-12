from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base 
import PIL.Image,io,os
import werkzeug,base64
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields, reqparse



app = Flask(__name__,template_folder='template')
db =  create_engine('postgresql+pg8000://root:root@localhost/demo')  
base = declarative_base()


class Image(base):  
    __tablename__ = 'imag_file'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)

class Multi(base):  
    __tablename__ = 'multi_file'

    id = Column(Integer, primary_key=True)
    img_id = Column(Integer,nullable = False)
    name = Column(String, nullable = False)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)



@app.route('/postfile',methods=["POST"])
def post():
    try:
        files = request.files.getlist('file[]') 
        name = request.form['name']
        path = os.path.join(os.getcwd()+"/static/images/",name)
        print(path)
        os.mkdir(path)
        for file in files:
            file.save(os.path.join(path,file.filename))
        new = Image(name=name)
        session.add(new)
        session.commit()
        image = session.query(Image).filter(Image.name == name).one()
        for file in files:
            img = Multi(img_id=image.id,name=file.filename)
            session.add(img)
        session.commit()
        return jsonify({"msg":"stored successfully"})
    except Exception as e:
        print(e)  

@app.route('/displayfile/<string:f_name>')
def get(f_name):
    image =session.query(Image).filter(Image.name == f_name).one()
    files = session.query(Multi).filter(Multi.img_id==image.id).all()
    image = []
    for file in files:
         name = file.name
         image.append(name)
    return render_template('img.html',images=image,name=f_name)
    
    
         
    


if __name__ == '__main__':
    app.run(debug=True)
