from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import  os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/quanlybanvemaybay'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Bán vé máy bay",
              template_mode='bootstrap4')

login = LoginManager(app=app)