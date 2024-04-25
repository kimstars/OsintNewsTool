from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from passlib.apps import custom_app_context as pwd_content
from models import *
from flask_restful import Api
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from model_detectfakenews import detect_fakenews

admin_web = Blueprint('admin_web', __name__, template_folder="templates", static_folder="static")
api = Api(admin_web)



@admin_web.route('/admin/', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin/index.html')


@admin_web.route('/admin/chart', methods=['GET', 'POST'])
def admin_chart():
    
    time = datetime.datetime.now()
    current_app.db.session.add(Category("Thoi su",time))
    current_app.db.session.commit()

    return render_template('admin/chart.html')


@admin_web.route('/admin/managernews', methods=['GET', 'POST'])
def view():
    
    query = Article.query.all()

    return render_template('admin/news_manager.html',listNews=query)



@admin_web.route('/admin/crawler', methods=['GET', 'POST'])
def crawler():
    
    if request.method == 'POST' and form.validate_on_submit():
        form = request.form
        url = form.get("url")
        
        #check urrl trong db , neu co check lai content
        # neu chua co -> crawl ve 
        
        

    return render_template('admin/news_manager.html',   )


@admin_web.route('/admin/summerize', methods=['GET', 'POST'])
def summerize():
    
    

    return render_template('admin/news_manager.html',  )



@admin_web.route('/admin/detectnews', methods=['GET', 'POST'])
def detectnews():
    data = {}
    
    if request.method == 'POST' and form.validate_on_submit():
        form = request.form
        url = form.get("url")
        data = detect_fakenews(url)

    return render_template('admin/thongtindetect.html', data=data )