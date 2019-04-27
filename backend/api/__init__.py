from flask import Flask
from flask_restful import Resource, Api
from utils.logger import Logger
import os

lumbrjak = Logger(__name__, filename='api.log')
LOG = lumbrjak.get_logger()

test_lumbrjak = Logger('test', 'test.log')

LOG.info('%s:%s' % (lumbrjak, test_lumbrjak))

app = Flask(__name__)
api = Api(app)

LOG.info('API created siccessfully ...')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')