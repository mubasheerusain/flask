from flask import *
from flask_mail import Mail,Message
import os

app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']='mohamed.hussain@atmecs.com'
app.config['MAIL_PASSWORD']='Mubasheerhussain@12345'

mail = Mail(app)


@app.route('/mail')
def sendMail():
   msg = Message('Hello', sender = 'mohamed.hussain@atmecs.com', recipients = ['sai.suryaprakash@atmecs.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   msg.html = render_template('se.html')
   mail.send(msg)
   return "Sent"


if __name__ == '__main__':
    app.run(debug = True)
