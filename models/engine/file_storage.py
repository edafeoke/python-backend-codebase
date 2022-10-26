#!/usr/bin/python3
"""file_storage module"""

from datetime import datetime
# import sys
# sys.path.append('../../models')
from models.base_model import BaseModel
# Import all models that inherit from base_model here
from models.user import User
from os.path import exists
import json


class FileStorage:
    """File Storage class"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        '''returns the dictionary __objects'''
        if cls:
            cls_objs = {}
            for k, v in self.__objects.items():
                class_name = v.__class__
                if cls == class_name:
                    cls_objs[k] = v
            return cls_objs
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with
        key <obj class name>.id"""

        k = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[k] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_dict = {}
        for k, v in self.__objects.items():
            val = v.to_dict()
            if '_sa_instance_state' in val.keys():
                del val['_sa_instance_state']
            json_dict[k] = val
        with open(self.__file_path, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(json_dict))

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ;"""

        file_exists = exists(self.__file_path)

        if file_exists:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                dict = json.loads(f.read())
                for k, value in dict.items():
                    cls = value["__class__"]
                    obj = eval(cls)(**value)
                    self.new(obj)

    def delete(self, obj=None):
        '''
        delete obj from __objects if it’s inside
        '''
        
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

