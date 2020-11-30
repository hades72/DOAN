from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import  os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/quanlybanvemaybay'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Ban Ve May Bay",
              template_mode='bootstrap3')