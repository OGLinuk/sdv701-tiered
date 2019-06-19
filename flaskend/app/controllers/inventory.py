from app import app, LOG
from flask import render_template, redirect, request
import requests
import json

API_PATH = 'http://tiered-backend:9125'

@app.route('/add_book', methods=['GET', 'POST'])
def serve_add_book():
    if request.method == 'POST':
        LOG.info('serve_add_book(POST)')

        book_type = request.values.get('book_type')
        genre = request.values.get('book_genre')
        name = request.values.get('book_name')
        description = request.values.get('book_description')
        price = request.values.get('book_price')
        condition = request.values.get('book_condition')
        in_stock = request.values.get('in_stock')

        payload = {
            'type': book_type,
            'genre': genre,
            'description': description, 
            'price': price,
            'in_stock': in_stock
        }
        if book_type == 'used':
            payload['condition'] = condition

        r = requests.put('{}/book/{}'.format(API_PATH, name), json=payload)
        LOG.info(r.json())

        return redirect('/list_inventory')

    LOG.info('serve_add_book(GET)')
    return render_template('/add_book.html')

@app.route('/edit_book', methods=['GET', 'POST'])
def serve_edit_book():
    if request.method == 'POST':
        LOG.info('serve_edit_book(POST)')

        book_name = request.values.get('old_book_name')
        book_type = request.values.get('book_type')
        genre = request.values.get('book_genre')
        name = request.values.get('book_name')
        description = request.values.get('book_description')
        price = request.values.get('book_price')
        condition = request.values.get('book_condition')
        in_stock = request.values.get('in_stock')

        payload = {
            'edit': True,
            'name': name,
            'type': book_type,
            'genre': genre,
            'description': description, 
            'price': price,
            'in_stock': in_stock
        }
        if book_type == 'used':
            payload['condition'] = condition

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=payload)
        LOG.info(r.json())

        return redirect('/list_inventory')

    LOG.info('serve_edit_book(GET)')

    book_name = request.args.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    LOG.info(book)

    return render_template('/edit_book.html', book=json.loads(book['book']))

@app.route('/delete_book', methods=['POST'])
def serve_delete_book():
    if request.method == 'POST':
        LOG.info('serve_delete_book(POST)')

        book_name = request.values.get('name')

        r = requests.delete('{}/book/{}'.format(API_PATH, book_name)).json()
        LOG.info(r)

        return redirect('/list_inventory')