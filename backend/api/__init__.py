from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_restful import Api
from utils.logger import Logger
import os

lumbrjak = Logger(__name__, filename='api.log')
LOG = lumbrjak.get_logger()

test_lumbrjak = Logger('test', 'test.log')

LOG.info('%s:%s' % (lumbrjak, test_lumbrjak))

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['MONGO_URI'] = os.environ.get('DB')

mongo = PyMongo(app)
database = mongo.db
books = database.books

book_1 = {
    "name": "The Plague Year",
    "description": "A journal of the black plague",
    "price": 10,
    "condition": "Used",
    "in_stock": True,
    "last_modified": str(datetime.now()),
}

book_2 = {
    "name": "Robinson Crusoe",
    "description": "A book about a castaway",
    "price": 50,
    "condition": "Used",
    "in_stock": True,
    "last_modified": str(datetime.now()),
}

book_3 = {
    "name": "Henry V",
    "description": "A play written by shakespear",
    "price": 30,
    "condition": "Used",
    "in_stock": True,
    "last_modified": str(datetime.now()),
}

dummy_books = [book_1, book_2, book_3]

for book in dummy_books:
    books.insert(book)

LOG.info(mongo.db.command('ismaster'))
LOG.info('API created siccessfully ...')

from api.resources import *

api.add_resource(book.BookList, '/books')
api.add_resource(book.Book, '/books/<string:book_name>')
api.add_resource(test.Test, '/<string:test>')