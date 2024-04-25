    
from flask import Flask
from pages import website
from admin_views import admin_web
from flask_sqlalchemy import SQLAlchemy
from database import db_session, init_db
from models import *
import os.path as op

    
    
    
init_db()
app = Flask(__name__)
app.config.from_object('settings')
app.register_blueprint(website)
app.register_blueprint(admin_web)
app.secret_key = app.config.get('secret_key', 'secret')
db = SQLAlchemy(app)
app.db = db
path = op.join(op.dirname(__file__), 'static')
