from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from app.admin import blueprint
from app.base.models import *
from app.admin.model_detect.crawlData import start_crawl, crawl_unoffical, crawl_offical
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
    
    listNews = []
    listurl= ""
    if request.method == 'POST':
        form = request.form
        listurl = form.get("listUrl")
        if(listurl is not None):
            listurl = listurl.split("\n")
            print(listurl)
            for url in listurl:
                data = start_crawl(url.strip())
                listNews.append(data)
                print(data)

    return render_template('admin/trangcaodulieu.html', listNews=listNews, predata=listurl )

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
        data = start_crawl(url)
        print(data)
    return render_template('admin/thongtindetect.html', data=data )


@blueprint.route('/admin/search', methods=['GET', 'POST'])
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
    

 
@blueprint.route('/admin/cluster_news', methods=['GET', 'POST'])
def cluster_news():
    result = crawl_offical()
    
    return render_template('admin/ketquaphancum.html',result=result )



@blueprint.route('/admin/article/<int:article_id>', methods=['GET', 'POST'])
def one_article(article_id):
    
    article = Article.query.get(article_id)
    keywords = ", ".join([keyword.name for keyword in article.keywords])
    return render_template('admin/chitietbaibao.html',data=article, keywords=keywords )



# 3-----------------------------
@blueprint.route('/test', methods=['GET', 'POST'])
def test_keyword():
    article = Article.query.get(1)
    keywords = [keyword.name for keyword in article.keywords]
    print(keywords)
    return jsonify(keywords)
    
# @blueprint.route('/admin/add_keyword/<article_id>/<keyword_name>', methods=['GET'])


