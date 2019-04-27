from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from utils.logger import Logger
import os

lumbrjak = Logger(__name__, filename='app.log')
LOG = lumbrjak.get_logger()

test_lumbrjak = Logger('test', 'test.log')

LOG.info('%s:%s' % (lumbrjak, test_lumbrjak))

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.secret_key = os.urandom(24)
app.config['MONGO_URI'] = os.environ.get('DB')
CORS(app)

mongo = PyMongo(app)
database = mongo.db
todos = database.todo

LOG.info(mongo.db.command('ismaster'))
LOG.info('Application successfully created ...')

from app.controllers import *