from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text, Table
import datetime

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    url = Column(String(255))
    image_url = Column(String(255))
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    sentiment = Column(String(50))
    is_fake = Column(Boolean, default=False)

    category = relationship('Category', backref='articles')
    events = relationship('Event', secondary='article_event', back_populates='articles')
    keywords = relationship('Keyword', secondary='article_keyword', back_populates='articles')

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
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False)

    articles = relationship('Article', secondary='article_event', back_populates='events')
    
    def __init__(self, name, description, created_at):
        self.name = name
        self.description = description
        self.created_at = created_at



article_event_association = Table(
    'article_event',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    articles = relationship('Article', secondary='article_keyword', back_populates='keywords')

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at


article_keyword_association = Table(
    'article_keyword',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)
