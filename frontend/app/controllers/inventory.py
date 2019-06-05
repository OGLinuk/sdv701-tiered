from app import app, LOG
from flask import render_template, redirect, request
import requests
import json

@app.route('/new_books', methods=['GET'])
def serve_new_books():
    LOG.info('serve_new_books(GET)')

    book_list = requests.get('http://tiered-sdv701-backend:9124/books/new').json()

    if book_list['response'] == 'error':
        return render_template('/inventory.html', error='No inventory list found')

    return render_template('/new_books.html', books=json.loads(book_list['books']))

@app.route('/used_books', methods=['GET'])
def serve_used_books():
    LOG.info('serve_used_books(GET)')

    book_list = requests.get('http://tiered-sdv701-backend:9124/books/used').json()

    LOG.info(book_list)

    if book_list['response'] == 'error':
        return render_template('/inventory.html', error='No inventory list found')

    return render_template('/used_books.html', books=json.loads(book_list['books']))


@app.route('/add_book', methods=['GET', 'POST'])
def serve_add_book():
    if request.method == 'POST':
        LOG.info('serve_add_book(POST)')

        name = request.values.get('book_name')
        description = request.values.get('book_description')
        price = request.values.get('book_price')
        condition = request.values.get('book_condition')
        in_stock = request.values.get('in_stock')

        payload = {
            'description': description, 
            'price': price,
            'in_stock': in_stock
        }
        if condition:
            payload['condition'] = condition

        r = requests.put('http://tiered-sdv701-backend:9124/book/%s' % (name), json=payload)

        LOG.info(r.json())

        return redirect('/inventory')

    LOG.info('serve_add_book(GET)')
    return render_template('/add_book.html')