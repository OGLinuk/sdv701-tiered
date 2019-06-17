from app import app, LOG
import os

if __name__ == '__main__':
    HOST = os.environ.get('WEB_HOST', '0.0.0.0')
    PORT = os.environ.get('WEB_PORT', 7777)
    
    LOG.info('Application running on %s:%s' % (HOST, PORT))
    app.run(host=HOST, port=PORT)