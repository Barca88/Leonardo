from pymongo import MongoClient
from collections import OrderedDict
import sys

client = MongoClient()   # supply connection args as appropriate
db = client.leonardo

############################# ERRORS #############################

# Create if it doesn't exists
if 'imported_errors' not in db.list_collection_names():
    db.create_collection("imported_errors")  # Force create!

errors = {"$jsonSchema":
  {
         "bsonType": "object",
         "required": [ "header", "message", "type" ],
         "properties": {
             "id": {
                 "bsonType": "int",
                 "description": "describes the error"
                 },
             "header": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "message": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "type": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "confirmB": {
                 "bsonType": "bool",
                 "description": "describes the error"
                 },
            "createdAt": {
               "bsonType": "string",
                 "description": "describes the error"
                }
         }
  }
}

cmd = OrderedDict([('collMod', 'imported_errors'),
        ('validator', errors),
        ('validationLevel', 'moderate')])

db.command(cmd)
############################# INFOS #############################

# Create if it doesn't exists
if 'imported_info' not in db.list_collection_names():
    db.create_collection("imported_info")  # Force create!

info = {"$jsonSchema":
  {
         "bsonType": "object",
         "properties": {
             "type": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "name": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "number": {
                 "bsonType": "int",
                 "description": "describes the error"
                 },
             "date": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "size": {
                 "bsonType": "int",
                 "description": "describes the error"
                 }
         }
  }
}

cmd = OrderedDict([('collMod', 'imported_info'),
        ('validator', info),
        ('validationLevel', 'moderate')])

db.command(cmd)

############################# QUESTIONS #############################

# Create if it doesn't exists
if 'imported_questions' not in db.list_collection_names():
    db.create_collection("imported_questions")  # Force create!

# Create index to ensure id uniqueness
imported_questions_coll = db['imported_questions']
imported_questions_coll.create_index("id", unique=True)

imported_questions = {"$jsonSchema":
  {
         "bsonType": "object",
         "required": ["id"],
         "properties": {
             "id": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "language": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "study_cycle": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "scholarity": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "domain": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "subdomain": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "difficulty_level": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "author": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "display_mode": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "type": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "answering_time": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "repetitions": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "header": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "body": {
                 "bsonType": "array",
                 "description": "describes the error"
                 },
             "explanation": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "imagens": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "videos": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "source": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "notes": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "status": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "inserted_by": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "inserted_at": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "validated_by": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "validated_at": {
                 "bsonType": "string",
                 "description": "describes the error"
                 },
             "precedence": {
                 "bsonType": "array",
                 "description": "describes the error"
                 },
             "flag": {
                 "enum": [ "aproved", "rejected", "pending" ],
                 "description": "describes the error"
                 }
         }
  }
}

cmd = OrderedDict([('collMod', 'imported_questions'),
        ('validator', imported_questions),
        ('validationLevel', 'moderate')])

db.command(cmd)
