from app import app, LOG
from datetime import datetime
from flask import render_template, request, redirect
import requests
import json

@app.route('/admin', methods=['GET'])
def serve_admin():
    LOG.info('serve admin')
    return render_template('/admin.html')

@app.route('/inventory', methods=['GET'])
def serve_inventory():
    LOG.info('serve inventory')

    book_list = requests.get('http://tiered-backend:9124/books').json()

    LOG.info(book_list['books'])

    if book_list['response'] == 'error':
        return render_template('/inventory.html', books='No inventory list found')
    
    return render_template('/inventory.html', books=json.loads(book_list['books']))

@app.route('/orders', methods=['GET'])
def serve_orders():
    LOG.info('serve orders')
    return render_template('/orders.html')

@app.route('/add', methods=['GET', 'POST'])
def serve_add_book():
    if request.method == 'POST':
        LOG.info('serve add book (POST)')

        name = request.values.get('book_name'),
        description = request.values.get('book_description'),
        price = request.values.get('book_price'),
        condition = request.values.get('book_condition'),
        
        r = requests.put('http://tiered-backend:9124/books/%s' % (name), 
                        data={"book_description": description, 
                            "book_price": price, 
                            "book_condition": condition})
        
        return redirect('/inventory')

    LOG.info('serve add book (GET)')
    return render_template('/add.html')
