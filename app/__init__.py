from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.secret_key = os.urandom(24)

from app.controllers import *