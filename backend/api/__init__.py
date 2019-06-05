from api.models import books
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_restful import Api
from utils.logger import Logger
import os

# Logger instantiation
lumbrjak = Logger(__name__, filename='api.log')
test_lumbrjak = Logger('test', 'test.log')

LOG = lumbrjak.get_logger()
LOG.info('%s:%s' % (lumbrjak, test_lumbrjak))

# App/api initialization
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.secret_key = os.urandom(24)
CORS(app)
api = Api(app)

# Database connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)
database = mongo.db
books_collection = database.books

# Dummy data
book_1 = books.UsedBook({
    'type': 'used',
    'name': "The Plague Year",
    'description': "A journal of the black plague",
    'price': 10,
    'in_stock': 7,
    'condition': 0,
    'last_modified': str(datetime.now())
})

book_2 = books.UsedBook({
    'type': 'used',
    'name': 'Robinson Crusoe',
    'description': 'A book about a castaway',
    'price': 50,
    'in_stock': 5,
    'condition': 1,
    'last_modified': str(datetime.now())
})

book_3 = books.NewBook({
    'type': 'new',
    'name': 'Henry V',
    'description': 'A play written by shakespear',
    'price': 30,
    'in_stock': 3,
    'last_modified': str(datetime.now())
})

# Inserting dummy data
dummy_books = [book_1, book_2, book_3]
for b in dummy_books:
    books_collection.insert(b)

# Test the mongo connection
LOG.info(mongo.db.command('ismaster'))

# Route definitions
from api.resources import *
api.add_resource(book.BookList, '/books/<string:book_type>')
api.add_resource(book.Book, '/book/<string:book_name>')
api.add_resource(test.Test, '/')

LOG.info('API created siccessfully ...')