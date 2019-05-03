from app import app, LOG
from flask import render_template

@app.route('/')
def serve_index():
    LOG.info('serve_index')
    return render_template('/index.html')