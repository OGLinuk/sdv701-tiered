from app import app, LOG
from flask import render_template, redirect, request
import requests
import json

API_PATH = 'http://tiered-backend:9125'

@app.route('/order_book', methods=['GET', 'POST'])
def serve_order_book():
    if request.method == 'POST':
        LOG.info('serve_order_book(POST)')

        order_quantity = request.values.get('quantity')
        book_name = request.values.get('name')
        customer_name = request.values.get('customer_name')
        customer_address = request.values.get('customer_address')

        book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
        book = json.loads(book['book'])

        book['in_stock'] -= int(order_quantity)

        book_payload = {
            'edit': True,
            'name': book['name'],
            'type': book['type'],
            'genre': book['genre'],
            'description': book['description'], 
            'price': book['price'],
            'in_stock': book['in_stock']
        }
        if book['type'] == 'used':
            book_payload['condition'] = book['condition']

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=book_payload)
        LOG.info(r.json())

        order_payload = {
            'book_id': book['_id']['$oid'],
            'order_quantity': order_quantity,
            'customer_name': customer_name,
            'customer_address': customer_address
        }

        r = requests.put('{}/order/{}'.format(API_PATH, book_name), json=order_payload)
        LOG.info(r.json())

        return render_template('/customer.html', status='Order placed successfully ...')

    LOG.info('serve_order_book(GET)')

    book_name = request.args.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    LOG.info(book)

    return render_template('/place_order.html', book=json.loads(book['book']))

@app.route('/delete_order', methods=['GET'])
def serve_delete_order():
    LOG.info('serve_delete_order(GET)')

    order_id = request.args.get('oid')
    book_id = request.args.get('bid')
    book_name = request.args.get('bname')

    payload = {
        'order_id': order_id,
        'book_id': book_id
    }

    r = requests.delete('{}/order/{}'.format(API_PATH, book_name), json=payload).json()
    LOG.info(r)

    return redirect('/list_orders')