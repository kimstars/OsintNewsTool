

from app.base.models import *
from app import db

def get_info_url(keyword):
    
    data = Article.query.filter(Article.title.contain(keyword)).all()

    print(keyword)
    result = []
    for item in data:
        temp = {
            "url" : item.url,
            "content" : item.content,
            "title" : item.title,
            "id": item.id
        }
        
        result.append(temp)
        
    return {
            "soketqua": len(result),
            "listdata" : result
            
            }


import bm25

def bm25_search(queries, docs):
    query_texts = [bm25.Text(query) for query in queries]
    doc_texts = [bm25.Document(doc) for doc in docs]
    
    bm25_obj = bm25.BM25(query_texts, doc_texts)
    scores = []
    for doc in doc_texts:
        score = bm25_obj.score(doc, query_texts[0], len(doc_texts))
        scores.append(score)
    return scores


from underthesea import word_tokenize


# Tìm kiếm Fulltextsearch với thuật toán bm25
def search_bm25(terms):
    queries = word_tokenize(terms)
    print(queries)
    texts = [item.content for item in Article.query.all()]
    scores = bm25_search(queries, texts)
    print(scores)
    max_score_index = max(range(len(scores)), key=scores.__getitem__)

    item  = Article.query.filter_by(id=max_score_index).first()
    temp = {}
    if(item):
        temp = {
            "url" : item.url,
            "content" : item.content,
            "title" : item.title,
            "id": item.id
        }
    return temp

def checkExist(url):
    existing_article = Article.query.filter_by(url=url).first()
    if existing_article:
        print("Da ton tai !", url)
        return existing_article
    else:
        return None

def InsertArticle(data):
    # Kiểm tra xem bài viết đã tồn tại trong cơ sở dữ liệu hay chưa
    existing_article = Article.query.filter_by(url=data['url']).first()

    if existing_article:
        # Cập nhật thông tin của bài viết
        for key, value in data.items():
            setattr(existing_article, key, value)
        db.session.commit()
        return existing_article.id
    else:
        # Thêm mới bài viết vào cơ sở dữ liệu
        new_article = Article(**data)
        db.session.add(new_article)
        db.session.commit()
        return new_article
        


def add_keyword_to_article(article_id, keyword_name):
    try:
        article = Article.query.get(article_id)
        keyword = Keyword.query.filter_by(name=keyword_name).first()
        if not keyword:
            keyword = Keyword(name=keyword_name)
            db.session.add(keyword)
        article.keywords.append(keyword)
        db.session.commit()
        return True
    except Exception as e:
        print("[Add keyword] error =>", e)
        return False




