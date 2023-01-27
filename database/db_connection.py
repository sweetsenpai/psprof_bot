import sqlalchemy as db

engine = db.create_engine('sqlite:///psprof.db')

connection = engine.connect()
metadata = db.MetaData()


topics = db.Table('topics', metadata,
                  db.Column('topic_id', db.Integer, primary_key=True),
                  db.Column('chat_id', db.Integer),
                  db.Column('name', db.CHAR(100)))
# masters = db.Table('Masters', metadata,
#                    db.Column('master_id', db.Integer, primary_key=True),
#                    db.Column('chat_master_id', db.Integer, ))
metadata.create_all(engine)