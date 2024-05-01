from flask import render_template, current_app
from app.base.models import *
from app.base import blueprint



def getNavBar():
    categories = Category.query.all()
    print(categories)  
    return categories



@blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')




    
    
   
    
    
import csv
import json

def csv_to_json(csv_file_path):
    data = []
    with open(csv_file_path, 'r', encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

@blueprint.route('/admin/loaddata', methods=['GET', 'POST'])
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
        # InsertArticle(data)
        print(data)
        dbdata.append(data)
        
    return str(data)
    
    
@blueprint.route('/delete/', methods=['GET', 'POST'])
def delete_fromdb():
    article_id = 4241
    article = Article.query.get(article_id)
    if article:
        db.session.delete(article)
        db.session.commit()
    
    keywords_to_delete = Keyword.query.filter(Keyword.id > 1).all()
    for keyword in keywords_to_delete:
        print(keyword.name)
        db.session.delete(keyword)
    db.session.commit()
    
    return 'Keywords with id greater than 2 have been deleted successfully'

    
