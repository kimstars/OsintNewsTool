from flask import Flask
from flask_admin import Admin
from pages import website
from flask_sqlalchemy import SQLAlchemy
from database import db_session, init_db, delete_db
from models import *
from datetime import timedelta
from flask_mail import Mail
import os.path as op




def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(website)
    app.secret_key = app.config.get('secret_key', 'secret')
    app.db = SQLAlchemy(app)
    path = op.join(op.dirname(__file__), 'static')
    
    
  
    return app



def main():
    app = create_app()
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    debug = app.config.get('DEBUG')
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    init_db()
    main()