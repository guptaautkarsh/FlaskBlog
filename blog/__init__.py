from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app) #database instance
bcrypt = Bcrypt(app) #Bcrypt class instance
login_manager = LoginManager(app) #LoginManager class instance
login_manager.login_view = 'login' #login func , to specify where login route is to be used in login required
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com' #SMTP server
app.config['MAIL_PORT'] = 587 #TLS PORT Number
app.config['MAIL_USE_TLS'] = True #using TLS
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('APP_PASSWORD') #App password
mail = Mail(app)

from blog import routes