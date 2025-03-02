from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Инициализация Flask и его расширений
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "taskhand"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes