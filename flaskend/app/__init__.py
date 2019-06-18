from flask import Flask
from flask_cors import CORS
from utils.logger import Logger
import os

# Logger instantiation
lumbrjak = Logger(__name__, filename='flaskend.log')
test_lumbrjak = Logger('test', 'test.log')

LOG = lumbrjak.get_logger()
LOG.info('%s:%s' % (lumbrjak, test_lumbrjak))

# App initialization
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.secret_key = os.urandom(24)
CORS(app)

from app.controllers import *

LOG.info('Application successfully created ...')