from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from app.admin import blueprint
from app.base.models import *
from app.admin.model_detectfakenews import detect_fakenews
from app import db
from .handle import *
from app.admin.model_detect.crawlData import start_crawl
from datetime import datetime 

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
    artical={}
    
    if request.method == 'POST':
        url_crawler = request.form.get("form_name")  # Lấy tên của biểu mẫu
        print(url_crawler)
        print("--------------------------")
        artical = Article.query.filter_by(url=url_crawler).first()
        if not artical:
            #crawler
            result = start_crawl(url_crawler)
            # print(result)

            title_=result.get("title")
            
            content_ = result.get("content")
            published_date_str= result.get("published_date")
            print("================")
            # nếu mà ngày này mà rỗng thì cho là ngày crawl về nha
            if published_date_str:  # Nếu chuỗi không rỗng
                try:
                    # Chuyển đổi chuỗi thành đối tượng datetime
                    published_datetime = datetime.strptime(published_date_str, "%y-%m-%d %H:%M:%S")
                    # Đối tượng datetime có thể được chuyển đổi thành date object nếu bạn chỉ quan tâm đến ngày
                    published_date = published_datetime.date()
                except ValueError:
                    print("Chuỗi ngày tháng không đúng định dạng.")
            else:
                # Nếu chuỗi rỗng, đặt published_date bằng ngày hôm nay
                published_date = datetime.now()
            # published_date=datetime.now()
            print ("====================")
            print(published_date)
            published_date_=published_date
            data = detect_fakenews(url_crawler)
            if data =="Safe news":
                is_fake=0
            else:
                is_fake=1

            new_article = Article(title = title_, url = url_crawler ,  content=content_, is_fake=is_fake ,image_url=result.get("top_img"), author="", category_id="",summerize="", created_at=published_date)
            
            # Thêm bài báo vào session
            db.session.add(new_article)
            
            # Commit thay đổi vào cơ sở dữ liệu
            db.session.commit()
        # print(artical)
        #check urrl trong db , neu co check lai content
        # neu chua co -> crawl ve 
    return render_template('admin/crawler1.html',  data=artical )



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
        # print(data)
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


