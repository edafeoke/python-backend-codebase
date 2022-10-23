#!/usr/bin/python3
'''user module'''

from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    '''User class'''

    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
