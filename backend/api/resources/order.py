from api import books_collection, LOG, orders_collection
from api.models import orders, books
from bson import json_util, ObjectId
from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from pymongo import ReturnDocument
import json

class Order(Resource):
    def put(self, book_name):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', type=str, help='ID of book')
        parser.add_argument('order_quantity', type=int, help='Quantity of order')
        parser.add_argument('customer_name', type=str, help='Name of customer')
        parser.add_argument('customer_address', type=str, help='Address of customer')
        args = parser.parse_args()

        book = books_collection.find_one({'_id': ObjectId(args['book_id'])})

        book_order = orders.Order({
            'book_id': args['book_id'],
            'book_name': book_name,
            'order_price': book['price'] * float(args['order_quantity']),
            'order_quantity': args['order_quantity'],
            'last_modified': str(datetime.now()),
            'customer_name': args['customer_name'],
            'customer_address': args['customer_address']
        })

        if not book_name:
            return {'response': 'error'}, 400

        orders_collection.insert(book_order)

        return {'response': 'success', 
            'order': json.dumps(book_order, default=json_util.default)}, 201

    def delete(self, book_name):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type=str, help='ID of order')
        parser.add_argument('book_id', type=str, help='ID of book')
        args = parser.parse_args()

        book_doc = books_collection.find_one({'_id': ObjectId(args['book_id'])})
        order_doc = orders_collection.find_one({'_id': ObjectId(args['order_id'])})

        # Updating book with un-purchased stock
        book_doc['in_stock'] += order_doc['order_quantity']
        
        genre = book_doc['genre']
        if isinstance(genre, int):
            genre = books.Genre(genre).name

        if book_doc['type'] == 'used':
    
            condition = book_doc['condition']
            if isinstance(condition, int):
                condition = books.Condition(book_doc['condition']).name

            book = books_collection.find_one_and_update(
                {'name': book_name},
                {
                    '$set': {
                        'name': book_doc['name'],
                        'type': book_doc['type'],
                        'genre': genre,
                        'description': book_doc['description'],
                        'price': book_doc['price'],
                        'in_stock': book_doc['in_stock'],
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
                        'name': book_doc['name'],
                        'type': book_doc['type'],
                        'genre': genre,
                        'description': book_doc['description'],
                        'price': book_doc['price'],
                        'in_stock': book_doc['in_stock'],
                        'last_modified': str(datetime.now())
                    }
                },
                return_document=ReturnDocument.AFTER
            )
        LOG.info(book)

        order_del = orders_collection.delete_one({'_id': ObjectId(args['order_id'])})
        LOG.info(order_del.raw_result)
        
        check = orders_collection.find_one({'_id': ObjectId(args['order_id'])})
        if check == None:
            return {'response': 'success'}, 200
        else:
            return {'response': 'error'}, 400

class OrderList(Resource):
    def get(self):
        order_list = [v for v in orders_collection.find({})]

        if not order_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'orders': json.dumps(order_list, default=json_util.default)}, 200