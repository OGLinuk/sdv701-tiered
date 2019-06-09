from app import app, LOG
from flask import render_template, redirect, request
import requests
import json

API_PATH = 'http://tiered-sdv701-backend:9124'

@app.route('/order_book', methods=['GET', 'POST'])
def serve_order_book():
    if request.method == 'POST':
        LOG.info('serve_order_book(POST)')

        order_quantity = request.values.get('quantity')
        book_name = request.values.get('name')

        book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
        book = json.loads(book['book'])

        book['in_stock'] -= int(order_quantity)

        payload = {
            'edit': True,
            'name': book['name'],
            'type': book['type'],
            'genre': book['genre'],
            'description': book['description'], 
            'price': book['price'],
            'in_stock': book['in_stock']
        }
        if book['type'] == 'used':
            payload['condition'] = book['condition']

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=payload)
        LOG.info(r.json())

        return redirect('/customer')

    LOG.info('serve_order_book(GET)')

    book_name = request.args.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    LOG.info(book)

    return render_template('/place_order.html', book=json.loads(book['book']))