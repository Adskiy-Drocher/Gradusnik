from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///pupil.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('surname', String),
    Column('health', String),
    Column('image_path', String)
)

#metadata.create_all(engine)

class User(object):
    def __init__(self, name, surname, health, image_path):
        self.name = name
        self.surname = surname
        self.health = health
        self.image_path = image_path



mapper(User, users_table)
