from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from lumbrjak import logger
import os

LOG = logger.get_logger(__name__, filename='output.log')

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