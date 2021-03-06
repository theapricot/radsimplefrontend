print("importing modules...")
print("> Flask")
from flask import Flask, session, flash, url_for, redirect, render_template, abort, make_response, request
print("> Flask-sqlalchemy")
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from sqlalchemy.schema import PrimaryKeyConstraint
print("> Flask-login")
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from natural.date import duration
#import locale

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://radius:radpass@localhost/radius'
app.config['SECRET_KEY'] = 'thesecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
#locale.setlocale(locale.LC_ALL, 'en_US')

class Users(db.Model):
    __tablename__ = 'radcheck'
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(64))
    attribute = db.Column(db.String(64))
    op = db.Column(db.String(2))
    password = db.Column('value', db.String(253))
    
    def __init__(self ,username , attribute, op, password):
        self.username = username
        self.attribute = attribute
        self.op = op
        self.password = password
        
    def __repr__(self):
        return '<Radius {} {}>'.format(self.attribute, self.username)
    
class Clients(db.Model):
    __tablename__ = 'nas'
    id = db.Column(db.Integer , primary_key=True)
    address = db.Column('nasname', db.String(128))
    shortname = db.Column(db.String(32))
    type = db.Column(db.String(32))
    ports = db.Column(db.Integer)
    secret = db.Column(db.String(60))
    server = db.Column(db.String(64))
    community = db.Column(db.String(50))
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Client {}>'.format(self.address)
    
class UserGroup(db.Model):
    __tablename__ = 'radusergroup'
    __table_args__ = (
        PrimaryKeyConstraint('username', 'groupname'),
    )
    username = db.Column(db.String(64))
    groupname = db.Column(db.String(64))
    priority = db.Column(db.Integer)
    
    def __repr__(self):
        return'<UserGroup: {} in {}>'.format(self.username, self.groupname)

class PostAuth(db.Model):
    __tablename__ = 'radpostauth'
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column('pass', db.String(64))
    reply = db.Column(db.String(32))
    authdate = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Auth: {}, {}>'.format(self.username, self.reply)
        
    def date(self):
        return self.authdate.strftime('%H:%M %b %m %Y')
        
    def duration(self):
        return duration(self.authdate)
    
class GroupReply(db.Model):
    __tablename__ = 'radgroupreply'
    id = db.Column(db.Integer , primary_key=True)
    groupname = db.Column(db.String(64))
    attribute = db.Column(db.String(64))
    op = db.Column(db.String(2))
    value = db.Column(db.String(253))
    
class Accounting(db.Model):
    __tablename__ = 'radacct'
    radacctid = db.Column(db.Integer , primary_key=True)
    acctsessionid = db.Column(db.String(64))
    acctuniqueid = db.Column(db.String(32))
    username = db.Column(db.String(64))
    groupname = db.Column(db.String(64))
    realm = db.Column(db.String(64))
    nasipaddress = db.Column(db.String(15))
    nasportid = db.Column(db.String(15))
    nasporttype = db.Column(db.String(32))
    acctstarttime = db.Column(db.DateTime)
    acctstoptime = db.Column(db.DateTime)
    acctsessiontime = db.Column(db.Integer)
    acctauthentic = db.Column(db.String(32))
    connectinfo_start = db.Column(db.String(50))
    connectinfo_stop = db.Column(db.String(50))
    acctinputoctets = db.Column(db.Integer)
    acctoutputoctets = db.Column(db.Integer)
    calledstationid = db.Column(db.String(50))
    callingstationid = db.Column(db.String(50))
    acctterminatecause = db.Column(db.String(32))
    servicetype = db.Column(db.String(32))
    framedprotocol = db.Column(db.String(32))
    framedipaddress = db.Column(db.String(15))
    acctstartdelay = db.Column(db.Integer)
    acctstopdelay = db.Column(db.Integer)
    xascendsessionsvrkey = db.Column(db.String(10))
    
@app.route('/', methods = ['GET','POST'])
def users():
    users = Users.query.all()
    if request.method == 'GET':
        return render_template('users.html', users = users)
    
    if 'add' in request.form:
        name = request.form['name']
        pw = request.form['pass']
        if name == '' or pw == '':
            return redirect(url_for('users'))
        else:
            user = Users(name, 'User-Password', ':=', pw)
            db.session.add(user)
    elif 'delete' in request.form:
        user = Users.query.get(int(request.form['name']))
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('users'))

@app.route('/accounting', methods = ['GET','POST'])
def accounting():
    access_log = PostAuth.query.order_by(desc(PostAuth.authdate)).all()
    return render_template('accounting.html', access_log = access_log)
    
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=5000)
