#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade='all, delete, delete-orphan')
    
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """returns the list of City instances with
            state_id equals to the current State.id"""
            city_list = []
            from models import storage
            model = storage.all(City)
            for values in model.values():
                if values.state_id == self.id:
                    city_list.append(values)
            return city_list
