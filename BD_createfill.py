import sys
import json
import pymongo
from BD_Cred import init_db


def readjson(jfile):
    with open(jfile, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("file: "+ jfile + " loaded")
    return data


def fill_authors(db):
    authors = readjson("authors.json")

    my_authors = db["authors"]
    try:  # drop the collection in case it already exists
      my_authors.drop()  
    except pymongo.errors.OperationFailure:
      print("An authentication error was received.")
      sys.exit(1)
    print("my_authors.drop() OK\n")

    try: 
        result = my_authors.insert_many(authors)
    except pymongo.errors.OperationFailure:
        print("An authentication error was received.")
        sys.exit(1)
    print("my_authors.insert_many() OK\n")

    result = my_authors.find()
    if result:    
      for doc in result:
        fullname = doc['fullname']
        born_date = doc['born_date']
        born_location = doc['born_location']
        print(f"> fullname: {fullname}; born_date: {born_date};\nborn_location: {born_location}")
    else:
      print("No authors found.")

    print("my_authors.find() OK\n")


def fill_qoutes(db):
    qoutes = readjson("qoutes.json")

    my_authors = db["authors"]
    for q in qoutes:
        q["author"] = my_authors.find_one({"fullname": q["author"]})['_id']
    
    my_qoutes = db["qoutes"]
    try:  # drop the collection in case it already exists
      my_qoutes.drop()  
    except pymongo.errors.OperationFailure:
      print("An authentication error was received.")
      sys.exit(1)
    print("my_qoutes.drop() OK\n")

    try: 
        result = my_qoutes.insert_many(qoutes)
    except pymongo.errors.OperationFailure:
        print("An authentication error was received.")
        sys.exit(1)
    print("my_qoutes.insert_many() OK\n")

    result = my_qoutes.find()
    if result:    
      for doc in result:
        tags = doc['tags']
        author = doc['author']
        qoute = doc['quote']
        print(f"author: {author}; tags: {tags};\nqoute: {qoute}")
    else:
      print("No qoutes found.")
    print("my_qoutes.find() OK\n")


def main():
    db = init_db()
    if db:
        fill_authors(db)
        fill_qoutes(db)


if __name__ == '__main__':
    main()