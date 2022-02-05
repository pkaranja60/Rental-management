from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b9f6ec740f5b4993a63813987c586757'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = f'You must be Logged in to view this page'
login_manager.login_message_category = "warning"

from rental import routes