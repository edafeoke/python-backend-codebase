#!/usr/bin/python3
'''db_storage module'''
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User



class DBStorage:
    '''DBStorage class'''

    __engine = None
    __session = None

    def __init__(self) -> None:
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('ENV')
        
        print(HBNB_MYSQL_USER)
        self.__engine = create_engine(f'mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}', echo=True, pool_pre_ping=True)
        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''query on the current database session'''
        if cls:
            o = {}
            objs = self.__session.query(cls).all()
            for obj in objs:
                k = f"{obj.__class__.__name__}.{obj.id}"
                o[k] = obj
        else:
            return self.__session.query().all()

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
