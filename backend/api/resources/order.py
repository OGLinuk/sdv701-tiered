from api import books_collection, LOG, orders_collection
from api.models import order
from bson import json_util, ObjectId
from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
import json

class Order(Resource):
    def put(self, book_id):
        parser = reqparse.RequestParser()
        
        parser.add_argument('order_quantity', type=int, help='Quantity of order')
        parser.add_argument('customer_name', type=str, help='Name of customer')
        parser.add_argument('customer_address', type=str, help='Address of customer')

        args = parser.parse_args()

        book = books_collection.find_one({'_id': ObjectId(book_id)})

        book_order = order.Order({
            'book_id': book_id,
            'book_name': book['name'],
            'order_price': book['price'] * float(args['order_quantity']),
            'order_quantity': args['order_quantity'],
            'last_modified': str(datetime.now()),
            'customer_name': args['customer_name'],
            'customer_address': args['customer_address']
        })

        if not book_id:
            return {'response': 'error'}, 400
        
        check = orders_collection.find_one({'_id': book_id})
        if check != None:
            return {'response': 'found existing', 
                    'book': json.dumps(check, default=json_util.default)}, 200

        orders_collection.insert(book_order)

        return {'response': 'success', 
            'order': json.dumps(book_order, default=json_util.default)}, 201

class OrderList(Resource):
    def get(self):
        order_list = [v for v in orders_collection.find({})]

        if not order_list:
            return {'response': 'error'}, 400

        return {'response': 'success', 
                'orders': json.dumps(order_list, default=json_util.default)}, 200