from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text
import datetime


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255))
    image_url = Column(String(255))
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    sentiment = Column(String(50))
    is_fake = Column(Boolean, default=False)

    category = relationship('Category', backref=backref('articles', lazy=True))
    events = relationship('Event', secondary='article_event', backref=backref('articles', lazy=True))
    keywords = relationship('Keyword', secondary='article_keyword', backref=backref('articles', lazy=True))

    def __init__(self, title, category_id, url, image_url, author, content, created_at, sentiment=None, is_fake=False):
        self.title = title
        self.category_id = category_id
        self.url = url
        self.image_url = image_url
        self.author = author
        self.content = content
        self.created_at = created_at
        self.sentiment = sentiment
        self.is_fake = is_fake

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at



class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name, description, created_at):
        self.name = name
        self.description = description
        self.created_at = created_at



class ArticleEvent(Base):
    __tablename__ = 'article_event'

    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)

    article = relationship("Article", back_populates="events")
    event = relationship("Event", back_populates="articles")

    def __init__(self, article_id, event_id):
        self.article_id = article_id
        self.event_id = event_id
        


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at


class ArticleKeyword(Base):
    __tablename__ = 'article_keyword'

    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)

    article = relationship("Article", back_populates="keywords")
    keyword = relationship("Keyword", back_populates="articles")

    def __init__(self, article_id, keyword_id):
        self.article_id = article_id
        self.keyword_id = keyword_id



    

