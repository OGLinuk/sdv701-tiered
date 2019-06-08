from app import app, LOG
from flask import render_template, request
import requests
import json

API_PATH = 'http://tiered-sdv701-backend:9124'

@app.route('/customer', methods=['GET'])
def serve_customer():
    LOG.info('serve_customer(GET)')
    return render_template('/customer.html')

@app.route('/search_inventory', methods=['GET', 'POST'])
def serve_search_inventory():
    if request.method == 'POST':
        LOG.info('serve_search_inventory(POST)')

        by_genre = request.values.get('search_by_genre')
        by_type = request.values.get('search_by_type')


        if by_genre != 'none':
            book_list = requests.get('{}/books_genre/{}'.format(API_PATH, by_genre)).json()
            LOG.info(book_list)

            if book_list['response'] == 'error':
                return render_template('/customer_inventory.html', error='No inventory list found')

        if by_type != 'none':
            book_list = requests.get('{}/books_type/{}'.format(API_PATH, by_type)).json()
            LOG.info(book_list)

            if book_list['response'] == 'error':
                return render_template('/customer_inventory.html', error='No inventory list found')
            
        return render_template('/customer_inventory.html', books=json.loads(book_list['books']))

    LOG.info('serve_search_inventory(GET)')
    return render_template('/customer_inventory.html')