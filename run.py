from app import app, LOG
import os

HOST = os.environ.get('WEB_HOST')
PORT = os.environ.get('WEB_PORT')

if __name__ == '__main__':
    if HOST == None and PORT == None:
        HOST = '0.0.0.0'
        PORT = 7777
    LOG.info('Application running on %s:%s' % (HOST, PORT))
    app.run(host=HOST, port=PORT)