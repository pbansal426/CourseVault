from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='coursevaultmail@gmail.com'
    app.config['MAIL_PASSWORD']="cvp101010"
    app.config['MAIL_USE_TLS'] =False
    app.config['MAIL_USE_SSL']=True
    global mail
    mail= Mail(app)





    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app

