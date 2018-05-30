from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from puddle.incog import SECRET_KEY

# Flask app

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puddle.db'

# Database

db = SQLAlchemy(app)

# Password hashing

bcrypt = Bcrypt(app)

# Login manager

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Hold your horses, bub. You'll need to log in before we let you continue."
login_manager.login_message_category = ''

from puddle import routes
