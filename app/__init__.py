from flask import Flask
from flask_cors import CORS
from lumbrjak import logger
import os

LOG = logger.get_logger(__name__, filename='output.log')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.secret_key = os.urandom(24)

LOG.info('Application successfully created ...')

from app.controllers import *