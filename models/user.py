#!/usr/bin/python3

from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class User(BaseModel, Base):
    '''User class'''

    __tablename__ = 'users'

    if HBNB_TYPE_STORAGE == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        # __tablename__ = 'users'
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
