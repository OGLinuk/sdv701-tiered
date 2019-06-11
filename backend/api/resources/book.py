from api import books_collection, LOG
from api.models import books
from bson import json_util
from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from pymongo import ReturnDocument
import json

class Book(Resource):
    def put(self, book_name):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, help='Type of book')
        parser.add_argument('genre', help='Genre of book')
        parser.add_argument('description', type=str, help='Description of book')
        parser.add_argument('price', type=float, help='Price of book')
        parser.add_argument('in_stock', type=int, help='Quantity of stock')
        parser.add_argument('condition', help='Condition of book')
        parser.add_argument('edit', type=bool, help='Check if editing book')
        parser.add_argument('name', type=str, help='New name if editing book')   
        args = parser.parse_args()

        if not book_name:
            return {'response': 'error'}, 400

        # TODO: Need to fix bug where condition remains when changing from used to new type 
        # Editing book
        if args['edit']:

            genre = args['genre']
            if isinstance(genre, int):
                genre = books.Genre(genre).name

            # Used book
            if args['type'] == 'used':

                condition = args['condition']
                if isinstance(condition, int):
                    condition = books.Condition(args['condition']).name

                book = books_collection.find_one_and_update(
                    {'name': book_name},
                    {
                        '$set': {
                            'name': args['name'],
                            'type': args['type'],
                            'genre': genre,
                            'description': args['description'],
                            'price': args['price'],
                            'in_stock': args['in_stock'],
                            'condition': condition,
                            'last_modified': str(datetime.now())
                        }
                    },
                    return_document=ReturnDocument.AFTER
                )
            # New book
            else:
                book = books_collection.find_one_and_update(
                    {'name': book_name},
                    {
                        '$set': {
                            'name': args['name'],
                            'type': args['type'],
                            'genre': genre,
                            'description': args['description'],
                            'price': args['price'],
                            'in_stock': args['in_stock'],
                            'last_modified': str(datetime.now())
                        }
                    },
                    return_document=ReturnDocument.AFTER
                )

            check = books_collection.find_one({'name': book['name']})
            if check != None:
                return {'response': 'found existing', 
                        'book': json.dumps(check, default=json_util.default)}, 200
            else:
                return {'response': 'error'}, 400

        # Adding book
        else:
            if args['type'] == 'used':
                book = books.UsedBook({
                    'name': book_name,
                    'type': args['type'],
                    'genre': int(args['genre']),
                    'description': args['description'],
                    'price': args['price'],
                    'in_stock': args['in_stock'],
                    'condition': int(args['condition']),
                    'last_modified': str(datetime.now())
                })
            else:
                book = books.NewBook({
                    'name': book_name,
                    'type': args['type'],
                    'genre': int(args['genre']),
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

            return {'response': 'success', 
                'book': json.dumps(book, default=json_util.default)}, 201

    def get(self, book_name):
        book = books_collection.find_one({'name': book_name})

        if not book:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'book': json.dumps(book, default=json_util.default)}, 200

    def delete(self, book_name):
        book_del = books_collection.delete_one({'name': book_name})
        LOG.info(book_del.raw_result)

        check = books_collection.find_one({'name': book_name})
        if check == None:
            return {'response': 'success'}, 200
        else:
            return {'response': 'error'}, 400

class BookList(Resource):
    def get(self):
        book_list = [v for v in books_collection.find({})]
        
        if not book_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'books': json.dumps(book_list, default=json_util.default)}, 200

class BookGenreList(Resource):
    def get(self, book_genre):
        book_list = [v for v in books_collection.find({'genre': book_genre})]

        if not book_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'books': json.dumps(book_list, default=json_util.default)}, 200

class BookTypeList(Resource):
    def get(self, book_type):
        book_list = [v for v in books_collection.find({'type': book_type})]
        
        if not book_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'books': json.dumps(book_list, default=json_util.default)}, 200