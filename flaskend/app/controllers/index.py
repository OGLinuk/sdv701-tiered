from app import app, LOG
from flask import render_template

@app.route('/', methods=['GET'])
def serve_index():
    LOG.info('serve_index(GET)')
    return render_template('/index.html')