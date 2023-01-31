import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Creat DataBase tables


class Topic(Base):
    __tablename__ = 'topics'
    topic_id = sql.Column(name='topic_id', type_=sql.Integer, primary_key=True)
    title = sql.Column(name='title', type_=sql.String)

    def __init__(self, topic_id, titel):
        self.topic_id = topic_id
        self.title = titel

    def __repr__(self):
        return f'{self.topic_id},{self.title}'


class Master(Base):
    __tablename__ = 'masters'
    master_id = sql.Column(name='master_id', type_=sql.Integer, primary_key=True)
    topic_master = sql.Column(sql.Integer, sql.ForeignKey('topics.topic_id'))
    info = sql.Column(name='info', type_=sql.String)

    def __int__(self, master_id, topic_master, info):
        self.master_id = master_id
        self.topic_master = topic_master
        self.info = info

    def __repr__(self):
        return f'{self.master_id}, {self.topic_master}, {self.info}'


class Review(Base):
    __tablename__ = 'reviews'
    review_id = sql.Column(name='review_id', type_=sql.Integer, primary_key=True)
    user_id = sql.Column(name='user_id', type_=sql.Integer)
    user_master = sql.Column(sql.Integer, sql.ForeignKey('masters.master_id'))
    user_name = sql.Column(name='user_name', type_=sql.String)
    review_text = sql.Column(name='review_text', type_=sql.String)
    review_rating = sql.Column(name='review_rating', type_=sql.Integer)
    review_moderation = sql.Column(name='review_moderation', type_=sql.BOOLEAN, default=False)

    def __int__(self, review_id, user_id, user_master, user_name, review_text, review_rating, review_moderation):
        self.review_id = review_id
        self.user_id = user_id
        self.user_master = user_master
        self.user_name = user_name
        self.review_text = review_text
        self.review_rating = review_rating
        self.review_moderation = review_moderation

    def __repr__(self):
        return f'{self.review_id}, {self.user_id}, {self.user_master},{self.user_name}, {self.review_text}, ' \
               f'{self.review_rating},{self.review_moderation}'


engine = sql.create_engine('sqlite:///psprof.db', echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
topic1 = Topic(topic_id=3, titel='A')
topic2 = Topic(topic_id=4, titel='B')
topic3 = Topic(topic_id=5, titel='C')
session.add_all([topic3, topic2, topic1])
session.commit()
print('---------------------')
result = session.query(Topic).order_by(Topic.topic_id).all()

for r in result:
    print(r)



