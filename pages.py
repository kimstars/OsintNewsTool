from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
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


def InsertArticle(data):
    try:
        temp = Article.query.filter_by(url=data['url']).first()
        if (temp):
            print("Da ton tai")
            return
    
    except Exception as e:
        print("Da ton tai 1")
        return
    
    
    new_article = Article(data['title'], 
                        data['url'],
                        data['image_url'],
                        data['author'],
                        data['category_id'],
                        data['content'],
                        data['summerize'],
                        data['create_at'],
                        data['sentiment'],
                        data['is_fake'],
                        )
    
    current_app.db.session.add(new_article)
    current_app.db.session.commit()
    
    
import csv
import json

def csv_to_json(csv_file_path):
    data = []
    with open(csv_file_path, 'r', encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

@website.route('/admin/loaddata', methods=['GET', 'POST'])
def test():
    datajson = csv_to_json("dataFakeNewsKhoi8406.csv")
    time = datetime.datetime.now()
    item = (datajson[0])
    
    dbdata = []
    
    for item in datajson:
        isfake = False
        if (item["label"] == "1"):
            isfake = True 
        data = {
            "title" : item["title"],
            "url" : item["url"],
            "image_url" : "",
            "author" : "",
            "category_id": 1,
            "content" : item["content"],
            "summerize" : "",
            "create_at" : time,
            "sentiment" : "",
            "is_fake" : isfake
        }
        InsertArticle(data)
        print(data)
        dbdata.append(data)
        
    return str(data)
    
    
@website.route('/admin/managernews', methods=['GET', 'POST'])
def view():
    
    query = Article.query.all()

    return render_template('admin/news_manager.html',listNews=query)