from app import app, LOG
from flask import render_template
import requests

@app.route('/customer', methods=['GET'])
def serve_customer():
    LOG.info('serve customer')
    return render_template('/customer.html')