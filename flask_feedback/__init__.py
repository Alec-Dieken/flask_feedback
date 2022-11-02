from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "0fedef89556952b5478fd3e883c77301"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user123:password123@localhost:5432/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_feedback import routes