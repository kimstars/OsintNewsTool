from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from app.admin import blueprint
from app.base.models import *
from app.admin.model_detectfakenews import detect_fakenews
from app import db
from .handle import *

@blueprint.route('/admin/', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin/index.html')


@blueprint.route('/admin/chart', methods=['GET', 'POST'])
def admin_chart():
    
    time = datetime.datetime.now()
    db.session.add(Category("Thoi su",time))
    db.session.commit()

    return render_template('admin/chart.html')


@blueprint.route('/admin/managernews', methods=['GET', 'POST'])
def view():
    
    query = Article.query.all()

    return render_template('admin/news_manager.html',listNews=query)



@blueprint.route('/admin/crawler', methods=['GET', 'POST'])
def crawler():
    
    if request.method == 'POST' and form.validate_on_submit():
        form = request.form
        url = form.get("url")
        
        #check urrl trong db , neu co check lai content
        # neu chua co -> crawl ve 

    return render_template('admin/news_manager.html',   )

from .tomtatvanban import Summerizer
@blueprint.route('/admin/summerize', methods=['GET', 'POST'])
def summerize():
    data = content= ""
    if request.method == 'POST':
        form = request.form
        content = form.get("content")
        numsentence = form.get("numsentence")
        data = Summerizer(content,int(numsentence))
        
    return render_template('admin/thongtintomtat.html', pre_data=content, data = data )



@blueprint.route('/admin/detectnews', methods=['GET', 'POST'])
def detectnews():
    data = {}
    
    if request.method == 'POST':
        form = request.form
        url = form.get("url")
        data = detect_fakenews(url)
        print(data)
    return render_template('admin/thongtindetect.html', data=data )


@blueprint.route('/admin/getInfoURL', methods=['GET', 'POST'])
def getInfoURL():
    data = {}
    url = ""
    if request.method == 'POST':
        form = request.form
        url = form.get("url")
        data = search_bm25(url)
        print(data)
    return render_template('admin/trangtimkiem.html'
                        #    , soketqua=data['soketqua'] ,data=data['listdata']
                           , keyword=url,
                           scores = data
                           )
    


# @blueprint.route('/admin/add_keyword/<article_id>/<keyword_name>', methods=['GET'])


