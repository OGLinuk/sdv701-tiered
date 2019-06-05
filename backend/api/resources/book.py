from api import books_collection, LOG
from api.models import books
from bson import json_util
from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
import json

class Book(Resource):
    def put(self, book_name):
        parser = reqparse.RequestParser()
        
        parser.add_argument('description', type=str, required=True, help='Description of book')
        parser.add_argument('price', type=int, required=True, help='Price of book')
        parser.add_argument('in_stock', type=int, required=True, help='Quantity of stock')
        parser.add_argument('condition', type=int, help='Condition of book')
        
        args = parser.parse_args()

        if not book_name:
            return {'response': 'error'}, 400
    
        if args['condition']:
            book = books.UsedBook({
                'type': 'used',
                'name': book_name,
                'description': args['description'],
                'price': args['price'],
                'in_stock': args['in_stock'],
                'condition': args['condition'],
                'last_modified': str(datetime.now())
            })
        else:
            book = books.NewBook({
                'type': 'new',
                'name': book_name,
                'description': args['description'],
                'price': args['price'],
                'in_stock': args['in_stock'],
                'last_modified': str(datetime.now())
            })

        check = books_collection.find_one({'name': book_name})
        if check != None:
            return {'response': 'found existing', 
                    'book': json.dumps(check, default=json_util.default)}, 200

        books_collection.insert(book)

        return {'response': 'success', 'book': json.dumps(book, default=json_util.default)}, 201

class BookList(Resource):
    def get(self, book_type):
        book_list = [v for v in books_collection.find({'type': book_type})]
        
        if not book_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'books': json.dumps(book_list, default=json_util.default)}, 200
