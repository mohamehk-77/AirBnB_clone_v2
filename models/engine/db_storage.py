#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.base_model import BaseModel
import os


class DBStorage:
    """DBStorage class that manages the database storage"""

    # private class attributes
    __engine = None
    __session = None

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    # public instance methods
    def __init__(self):
        """Constructor of the DBStorage class"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        connection_string = "mysql+mysqldb://{}:{}@{}/{}" .format(user, pwd, host, db)
        self.__engine = create_engine(connection_string, pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        from models import City

        dictionary = {}
        if cls is None:
            for cls_name in self.classes:
                query = self.__session.query(self.classes[cls_name])
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dictionary[key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dictionary[key] = obj
        return dictionary

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
