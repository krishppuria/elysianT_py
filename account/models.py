from config.dbConnection import db
from django.db import models
from datetime import datetime, timedelta
import boto3
from django.conf import settings
from bson import ObjectId
from django.db.models import Q

# --------------------------------------------------------------
# Account model
# --------------------------------------------------------------

class Account(models.Model):
    collection_name = 'users'
    
    @classmethod
    def create(cls, data):
        result = db[cls.collection_name].insert_one(data)
        return db[cls.collection_name].find_one({'_id': result.inserted_id},{'password':0})
    
    @classmethod
    def get(cls, email):
        return db[cls.collection_name].find_one({'email': email,"account": {'$ne': 'Inactive'}},{'_id': 0, 'password':0})
   
    
    @classmethod
    def getUserByEmail(cls, email):
        return db[cls.collection_name].find_one({'email': email})
    
    
    @classmethod
    def signIn(cls, email):
        return db[cls.collection_name].find_one({'email': email})

    


    
