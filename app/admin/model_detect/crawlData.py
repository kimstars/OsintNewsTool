import re
import json
import validators
from newspaper import Article
from bs4 import BeautifulSoup
from .todate import *

def is_url(url):
    return validators.url(url)

def clean_json(text):
    text = text.replace('"', '\\"').replace("\n"," ").replace("\t"," ").replace("\r"," ")
    text = re.sub(r'\s+', ' ', text)
    return text




# Function to extract the domain from a URL
def getDomain(url):
    split_url = url.split('/')
    return split_url[2]



import requests
from bs4 import BeautifulSoup, NavigableString
from fake_useragent import UserAgent

def crawler_viettan(url):
    def get_text_from_tag(tag):
        if isinstance(tag, NavigableString):
            return tag
        return tag.text
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    # url= "https://viettan.org/thu-di-tim-duong-cuu-nuoc/"
    while(True):
        try:
            response = requests.get(url, headers=headers)
            # print(response.status_code)
            code = response.status_code
            if(str(code) == "200"):
                break
        except :
            pass


    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1", class_="elementor-heading-title elementor-size-default").text
        
    # with open("output.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))

    author = soup.find("span",class_="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-author").text.strip()

    art_time = soup.find("span",class_="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date").text.strip()

    image = soup.find("div", class_="elementor-image").find('img')['src']

    divs = soup.find_all("div", class_="elementor-widget-container")
    content = ""
    for div in divs:
        paragraphs = (get_text_from_tag(p) for p in soup.find_all("p"))
        for p in paragraphs:
            content += p
            
    result = {
                'url': url,
                'title': title,
                'keywords': "",
                'author': author,
                'published_date': todatetime(art_time, 1),
                'top_img': image,
                'content': content
            }
    return result




from ..handle import InsertArticle, add_keyword_to_article

def start_crawl(url):
    domain = getDomain(url)
    
    if not is_url(url):
        result = {
            'url': url,
            'error': 'Url không hợp lệ!',
            'success': False
        }

        return result
    
    
    result = {}
    if("viettan.org" in domain):
        print("detect viettan ", url)
        result =  crawler_viettan(url)
    else:
        while(1):
            try:
                article = Article(url)
                article.download()
                article.parse()
                if(article):
                    break
            except:
                pass
        
        content = article.text
        
        if(content == ""):
            content = re.sub('\\n+', '</p><p>', '<p>' + clean_json(content) + '</p>')

        result = {
                    'url': url,
                    'error': '',
                    'success': True,
                    'title': article.title,
                    'keywords': ', '.join(article.keywords if article.keywords else (
                        article.meta_keywords if article.meta_keywords else article.meta_data.get('keywords', []))),
                    'published_date': article.publish_date if article.publish_date else article.meta_data.get('pubdate', ''),
                    'top_img': article.top_image,
                    'content': content
                }
    
    # them bai bao moi vao csdl
    print("kiet checkkk=====================================>",str(result['published_date']))
    # data = {
    #         "title" : result["title"],
    #         "url" : result["url"],
    #         "image_url" : result["top_img"],
    #         "author" : "",
    #         "category_id": 1,
    #         "content" : result["content"],
    #         "summerize" : "",
    #         "create_at" : result['published_date'],
    #         "sentiment" : "",
    #         "is_fake" : ""
    #     }
    # item_id = InsertArticle(data)
    
    # # them keyword
    # for key in result['keywords']:
    #     temp = key.lower().strip()
    #     ret = add_keyword_to_article(item_id, temp)
    #     print(f"{temp} => {ret}")
    
    return result

    
    