from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify, \
    make_response
from flask_security import login_required, logout_user, login_user, current_user, roles_accepted
from passlib.apps import custom_app_context as pwd_content
from models import *
# from forms import *
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
import os, datetime
from functools import wraps
from datetime import timedelta
from flask_restful import Api
from flask_cors import CORS
# from api.sources import ActorsListApi
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin

website = Blueprint('website', __name__)
api = Api(website)




def getNavBar():
    categories = Category.query.all()
    print(categories)  
    return categories





@website.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@website.route('/admin/', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin/index.html')


@website.route('/admin/chart', methods=['GET', 'POST'])
def admin_chart():
    
    time = datetime.datetime.now()
    current_app.db.session.add(Category("Thoi su",time))
    current_app.db.session.commit()
    
   
    return render_template('admin/chart.html')

@website.route('/admin/test', methods=['GET', 'POST'])
def test():
    
    time = datetime.datetime.now()
    first_data = Category.query.first()
    
    print(first_data.name)
    
    return first_data.name