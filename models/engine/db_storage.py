#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        usr = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(usr, pwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary"""
        dc = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for q in query:
                key = "{}.{}".format(type(q).__name__, q.id)
                dc[key] = q
        else:
            ls = [State, City, User, Place, Review, Amenity]
            for c in ls:
                query = self.__session.query(c)
                for q in query:
                    key = "{}.{}".format(type(q).__name__, q.id)
                    dc[key] = q
        return (dc)

    def save(self):
        """save changes"""
        self.__session.commit()

    def new(self, obj):
        """add a new element to the table"""
        self.__session.add(obj)


    def delete(self, obj=None):
        """delete an element from the table"""
        if obj:
            self.session.delete(obj)

    def close(self):
        """ close method"""
        self.__session.close()

    def reload(self):
        """configuration"""
        Base.metadata.create_all(self.__engine)
        S = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(S)
        self.__session = Session()
