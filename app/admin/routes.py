from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from app.admin import blueprint
from app.base.models import *
from app.admin.model_detect.crawlData import start_crawl, crawl_unoffical, crawl_offical, crawl_rss
from app.admin.model_detect.todate import *
from app import db
from .handle import *
from sqlalchemy import func
from datetime import datetime, timedelta

@blueprint.route('/admin/', methods=['GET', 'POST'])
def admin_home():
    # Bai viet moi them gan day
    recent_date = datetime.now() - timedelta(days=1)
    recent_art = Article.query.filter(func.DATE(Article.created_at) == func.DATE(recent_date)).all()

    
    sum_articles = Article.query.count()
    sum_categories = Category.query.count()
    sum_keywords= Keyword.query.count()

    #biểu đồ PIE tỉ lệ tin giả/ tin thật
    
    fn_fakeCount= Article.query.filter_by(is_fake=1).count()
    fn_realCount = Article.query.filter_by(is_fake=0).count()
    outfn_count =[fn_realCount,fn_fakeCount]
    
    # biểu đồ PIE Danh mục 
    categories = Category.query.distinct(Category.name).all()
    categories_name = [category.name for category in categories]
    category_counts = [Article.query.filter_by(category_id=category.id).count() for category in categories]
    print(category_counts)
    print(categories_name)
    fakeCounts=[]
    realCounts=[]


    for category in categories:
        fakeCount= Article.query.filter_by(category_id=category.id, is_fake=1).count()
        realCount = Article.query.filter_by(category_id=category.id, is_fake=0).count()
        fakeCounts.append(fakeCount)
        realCounts.append(realCount)
    print(fakeCounts,realCounts)
    
    
    # keywords = Keyword.query.all()
    # data_key = []
    # for item in keywords:
    #     count_temp = db.session.query(Article).join(Article.keywords).filter(Keyword.id==item.id).count()
    #     temp_data = {
    #         "name": item.name,
    #         "numart" : count_temp
    #     }
    #     data_key.append(temp_data)
      
    
    # top_keyword = sorted(data_key, key=lambda item: item['numart'], reverse=True)[:10]
    
    top_keyword = Keyword.query.limit(10).all()
    
    print(top_keyword)
    
    # Bieu do area -> Lay so luong bai bao 7 ngay gan day
    date, numNews = GetNumArtByDate()
    print("so luong bai bao 7 ngay gan day : ", date, numNews)
    
    
    return render_template('admin/index.html', sum_a=sum_articles, sum_c = sum_categories, sum_k=sum_keywords, categories=categories_name, category_data=category_counts, fakeCounts=fakeCounts, realCounts=realCounts,
    fnDataCount = outfn_count,
    listNews = recent_art,
    top10Keyword = top_keyword,
    dateLable = date, numNews = numNews
    )


@blueprint.route('/admin/chart', methods=['GET', 'POST'])
def admin_chart():
    
    time = datetime.datetime.now()
    db.session.add(Category("Thoi su",time))
    db.session.commit()

    return render_template('admin/chart.html')


@blueprint.route('/admin/managernews', methods=['GET', 'POST'])
def view():
    
    query = Article.query.limit(10).all()
    
    if request.method == 'POST':
        form = request.form
        startDate = form.get("startDate")
        endDate = form.get("endDate")
        print(startDate, type(startDate), endDate)
        query = Article.query.filter(func.DATE(Article.created_at) >= todatetime(startDate)).filter(func.DATE(Article.created_at) <= todatetime(endDate)).all()
        print("query thanh cong ", len(query))
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

    return render_template('admin/trangcaodulieu.html', listNews=listNews, predata=listurl, title="" )

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


# xem chi tiet bai bao
@blueprint.route('/admin/article/<int:article_id>', methods=['GET', 'POST'])
def one_article(article_id):
    
    article = Article.query.get(article_id)
    keywords = ", ".join([keyword.name for keyword in article.keywords])
    return render_template('admin/chitietbaibao.html',data=article, keywords=keywords )



#
@blueprint.route('/admin/cate_manager', methods=['GET', 'POST'])
def cate_manager():
    
    allCate = Category.query.all()
    dataCate = []
    for item in allCate:
        dataCate.append(
            {
                "id":item.id,
                "name":item.name,
                "numrss": db.session.query(RssPaper).filter_by(category_id=item.id).count(),
                "numart": db.session.query(Article).filter_by(category_id=item.id).count()

            }
        )
    
    
    return render_template('admin/cate_manager.html', listCates = dataCate  )

@blueprint.route('/admin/add_cate', methods=['POST'])
def add_cate():
    
    if request.method == 'POST':
        form = request.form
        newCate = form.get("newCate")
        InsertCategory(newCate)
        allCate = Category.query.all()
        return render_template('admin/cate_manager.html', listCates = allCate  )


@blueprint.route('/admin/rss_manager', methods=['GET'])
@blueprint.route('/admin/rss_manager/<int:cate_id>', methods=['GET'])
def rss_manager(cate_id=None):
    if request.method == 'GET':
        select = cate_id
        allRSS = RssPaper.query.all()
        print(allRSS)
        listCates = Category.query.all()
        return render_template('admin/rss_manager.html', listCates = listCates, listRSS= allRSS, valueSelect = select  )
    
@blueprint.route('/admin/add_rss', methods=['POST'])
def add_rss():
    if request.method == 'POST':
        form = request.form
        listRSS = form.get("listRSS")
        cate_id = form.get("cate_id")
        listRSS = listRSS.split("\n")
        for item in listRSS:
            if(item!= ""):
                url = item.strip()
                print("addrss => ",url)
                temp_data = {
                    "domain" : getDomain(url),
                    "url": url, 
                    "cate_id": cate_id
                }
                InsertRSS(temp_data)
        
        print('done add rss', len(listRSS))
            
        return redirect(url_for("admin.rss_manager"))

# xem chi tiet bai bao
@blueprint.route('/admin/rss_crawl/<int:rss_id>', methods=['GET', 'POST'])
def rss_crawl(rss_id):
    
    rssitem = RssPaper.query.get(rss_id)
    rssUrl = rssitem.url
    cate_id = rssitem.category.id
    listNews = crawl_rss(rssUrl, cate_id)
    print(len(listNews))
    return render_template('admin/trangcaodulieu.html', listNews=listNews, predata=[], title=rssUrl)




# 3-----------------------------
@blueprint.route('/test', methods=['GET', 'POST'])
def test_keyword():
    article = Article.query.get(1)
    keywords = [keyword.name for keyword in article.keywords]
    print(keywords)
    
    return jsonify(keywords)
    
# @blueprint.route('/admin/add_keyword/<article_id>/<keyword_name>', methods=['GET'])


# lay bai bao theo thoi gian

# keywords = Keyword.query.all()
# data_key = []
# for item in keywords:
#     count_temp = db.session.query(Article).join(Article.keywords).filter(Keyword.id==item.id).count()
#     temp_data = {
#         "name": item.name,
#         "numart" : count_temp
#     }
#     data_key.append(temp_data)



    