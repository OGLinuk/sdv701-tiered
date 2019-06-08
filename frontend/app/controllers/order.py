from app import app, LOG
from flask import render_template

@app.route('/order_book', methods=['GET', 'POST'])
def serve_order_book():
    return render_template('/place_order.html')