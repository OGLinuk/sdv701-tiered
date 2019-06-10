from app import app, LOG
from flask import render_template, request
import requests
import json

API_PATH = 'http://tiered-sdv701-backend:9124'

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

        LOG.info('PAYLOAD\n{}'.format(book_payload))

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=book_payload)
        LOG.info(r.json())

        order_payload = {
            'order_quantity': order_quantity,
            'customer_name': customer_name,
            'customer_address': customer_address
        }

        r = requests.put('{}/order/{}'.format(API_PATH, book['_id']['$oid']), json=order_payload)
        LOG.info(r.json())

        return render_template('/customer.html', status='Order placed successfully ...')

    LOG.info('serve_order_book(GET)')

    book_name = request.args.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    LOG.info(book)

    return render_template('/place_order.html', book=json.loads(book['book']))