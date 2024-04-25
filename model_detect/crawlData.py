import re
import json
import validators
from newspaper import Article
from bs4 import BeautifulSoup


def is_url(url):
    return validators.url(url)

def clean_json(text):
    text = text.replace('"', '\\"').replace("\n"," ").replace("\t"," ").replace("\r"," ")
    text = re.sub(r'\s+', ' ', text)
    return text

def crawl(url):
    if not is_url(url):
        result = {
            'url': url,
            'error': 'Url không hợp lệ!',
            'success': False
        }

        return result
    
    article = Article(url)
    article.download()
    article.parse()

    result = {
                'url': url,
                'error': '',
                'success': True,
                'title': article.title,
                'keywords': ', '.join(article.keywords if article.keywords else (
                    article.meta_keywords if article.meta_keywords else article.meta_data.get('keywords', []))),
                'published_date': article.publish_date if article.publish_date else article.meta_data.get('pubdate', ''),
                'top_img': article.top_image,
                'content': article.text
            }   
     
    return result
