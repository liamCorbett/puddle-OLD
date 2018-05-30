from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from puddle.incog import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puddle.db'
db = SQLAlchemy(app)

from puddle import routes