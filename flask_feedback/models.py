from functools import wraps
from flask import session, redirect, url_for
from flask_feedback import db, bcrypt

# DECORATOR FOR LOGIN ONLY PAGES
def login_required(func):

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if not 'user_id' in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    
    return wrapper_func

# BEGIN MODEL DEFINITIONS
class Users(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='users')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        return cls(username=username, password=password_hash, 
                    email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))