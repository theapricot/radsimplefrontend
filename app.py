print("importing modules...")
print("> Flask")
from flask import Flask, session, flash, url_for, redirect, render_template, abort, make_response, request
print("> Flask-sqlalchemy")
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
print("> Flask-login")
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://radius:radpass@192.168.1.157/radius'
app.config['SECRET_KEY'] = 'thesecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(64))
    attribute = db.Column(db.String(64))
    op = db.Column(db.String(2))
    value = db.Column(db.String(253))
    
if __name__ == '__main__':
    app.run(debug = True)
