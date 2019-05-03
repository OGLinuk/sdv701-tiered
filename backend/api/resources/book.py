from api import books, LOG
from bson import json_util
from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
import json

class Book(Resource):
    def put(self, book_name):
        parser = reqparse.RequestParser()
        parser.add_argument('book_description', type=str, required=True, help='Description of book')
        parser.add_argument('book_price', type=int, required=True, help='Price of book')
        parser.add_argument('book_condition', type=str, required=True, help='Condition of book')

        args = parser.parse_args()

        if not book_name:
            return {'response': 'error'}, 400
        
        book = {
            "name": book_name,
            "description": args['book_description'],
            "price": args['book_price'],
            "condition": args['book_condition'],
            "in-stock": True,
            "last modified": str(datetime.now())
        }

        check = books.find_one(book)
        if check != None:
            return {'response': 'found existing', 
                    'book': json.dumps(check, default=json_util.default)}, 200

        books.insert(book)

        return {'response': 'success', 'book': json.dumps(book, default=json_util.default)}, 201

class BookList(Resource):
    def get(self):
        book_list = [v for v in books.find({})]
        
        if not book_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'books': json.dumps(book_list, default=json_util.default)}, 200
