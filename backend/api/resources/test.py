from flask import request
from flask_restful import Resource
import socket

class Test(Resource):
    def get(self):
        return {'response': 'success', 'Hostname': socket.gethostname(), 
                'Address': socket.gethostbyname(socket.gethostname())}, 200