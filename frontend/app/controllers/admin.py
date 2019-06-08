from app import app, LOG
from flask import render_template
import requests
import json

API_PATH = 'http://tiered-sdv701-backend:9124'

@app.route('/admin', methods=['GET'])
def serve_admin():
    LOG.info('serve_admin(GET)')
    return render_template('/admin.html')

@app.route('/list_inventory', methods=['GET'])
def serve_inventory():
    LOG.info('serve_inventory(GET)')
        
    book_list = requests.get('{}/books'.format(API_PATH)).json()
    LOG.info(book_list)

    if book_list['response'] == 'error':
        return render_template('/admin_inventory.html', error='No inventory list found')

    return render_template('/admin_inventory.html', books=json.loads(book_list['books']))

@app.route('/list_orders', methods=['GET'])
def serve_orders():
    LOG.info('serve_orders(GET)')
    return render_template('/orders.html')
