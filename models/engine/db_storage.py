#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages storage of hbnb
     models in mySQL database using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """constructor"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                        format(getenv("HBNB_MYSQL_USER"),
                                            getenv("HBNB_MYSQL_PWD"),
                                            getenv("HBNB_MYSQL_HOST"),
                                            getenv("HBNB_MYSQL_DB")),
                                        pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        
    def all(self, cls=None):
        """query on the current database session"""
        result = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            for cls_query in self.__session.query(cls):
                key = f"{type(cls_query).__name__}.{cls_query.id}"
                result[key] = cls_query
            return result
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for obj in classes:
                for all_query in self.__session.query(obj):
                    key = f"{type(all_query).__name__}.{all_query.id}"
                    result[key] = all_query
            return result

    def new(self, obj):
        """ add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
