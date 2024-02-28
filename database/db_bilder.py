import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


db_path = 'sqlite:///' + os.environ.get("DB")
Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topics'
    topic_id = sql.Column(name='topic_id', type_=sql.Integer, primary_key=True)
    title = sql.Column(name='title', type_=sql.String)

    def __init__(self, topic_id, titel):
        self.topic_id = topic_id
        self.title = titel

    def __repr__(self):
        return f'{self.topic_id}, {self.title}'


class Master(Base):
    __tablename__ = 'masters'
    master_id = sql.Column(name='master_id', type_=sql.Integer, primary_key=True)
    topic_master = sql.Column(sql.Integer, sql.ForeignKey('topics.topic_id', ondelete="CASCADE"))
    msg_id = sql.Column(name='msg_id', type_=sql.Integer)
    company_name = sql.Column(name='company_name', type_=sql.String)
    name = sql.Column(name='name', type_=sql.String)
    phone = sql.Column(name='phone', type_=sql.String)
    Telegram = sql.Column(name='Telegram', type_=sql.String)
    addres = sql.Column(name='addres', type_=sql.String)
    specialization = sql.Column(name='specialization', type_=sql.String)
    optional = sql.Column(name='optional', type_=sql.String)
    tg_url = sql.Column(name='tg_url', type_=sql.String)

    def __int__(self, master_id, msg_id, topic_master, company_name, name, Telegram, phone, addres, specialization, optional, tg_url):
        self.master_id = master_id
        self.msg_id = msg_id
        self.topic_master = topic_master
        self.company_name = company_name
        self.name = name
        self.phone = phone
        self.telegram = Telegram
        self.addres = addres
        self.specialization = specialization
        self.optional = optional
        self.tg_url = tg_url

    def __repr__(self):
        return f'{self.master_id},{self.msg_id} ,{self.topic_master}, {self.company_name},{self.name}, {self.Telegram},' \
               f' {self.phone}, {self.addres},' \
               f' {self.addres}, {self.specialization}, {self.optional}, {self.tg_url}'

    def __msgdict__(self):
        return {'Компания': self.company_name, 'Имя': self.name, 'Номер': self.phone, 'Телеграм': self.Telegram,
                'Адрес': self.addres, 'Специализация': self.specialization,
                'Дополнительно': self.optional, 'Ссылка на телеграм': self.tg_url}

    def __to_dict__(self):
        return {'company_name': self.company_name, 'name': self.name, 'phone': self.phone, 'Telegram': self.Telegram, 'addres': self.addres,
                'specialization': self.specialization, 'optional': self.optional, 'tg_url': self.tg_url}


class Review(Base):
    __tablename__ = 'reviews'
    review_id = sql.Column(name='review_id', type_=sql.Integer, primary_key=True)
    user_id = sql.Column(name='user_id', type_=sql.Integer)
    user_master = sql.Column(sql.Integer, sql.ForeignKey('masters.master_id', ondelete="CASCADE"))
    user_name = sql.Column(name='user_name', type_=sql.String)
    review_text = sql.Column(name='review_text', type_=sql.String)
    review_rating = sql.Column(name='review_rating', type_=sql.Integer)
    review_moderation = sql.Column(name='review_moderation', type_=sql.BOOLEAN, default=False)
    time = sql.Column(name='time', type_=sql.String, nullable=True)

    def __int__(self, review_id, user_id, user_master, user_name, review_text, review_rating, review_moderation, time):
        self.review_id = review_id
        self.user_id = user_id
        self.user_master = user_master
        self.user_name = user_name
        self.review_text = review_text
        self.review_rating = review_rating
        self.review_moderation = review_moderation
        self.time = time

    def __repr__(self):
        return f'{self.review_id}, {self.user_id}, {self.user_master},{self.user_name}, {self.review_text}, ' \
               f'{self.review_rating},{self.review_moderation}'


if not os.path.exists(db_path):
    engine = sql.create_engine('sqlite:///psprof.db', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
else:
    engine = sql.create_engine(db_path, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()



