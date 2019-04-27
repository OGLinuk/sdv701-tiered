from api import app, LOG
import os

if __name__ == '__main__':
    HOST = os.environ.get('API_HOST', '0.0.0.0')
    PORT = os.environ.get('API_PORT', 7776)
    
    LOG.info('Application running on %s:%s' % (HOST, PORT))
    app.run(host=HOST, port=PORT)