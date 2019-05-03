from flask import request
from flask_restful import Resource
import socket

class Test(Resource):
    def get(self, test):
        if not test:
            return {'response': 'no test value'}, 400
            
        return {'response': 'success', 'Hostname': socket.gethostname(), 
                'Address': socket.gethostbyname(socket.gethostname()), 'test': test}, 200