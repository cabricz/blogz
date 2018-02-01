from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://blogz:blogz@localhost:8889/blogz"
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "2PJeO9VGXOoJTl"

db = SQLAlchemy(app)