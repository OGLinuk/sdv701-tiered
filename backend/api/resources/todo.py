from api import todos, LOG
from bson import json_util
from flask import request
from flask_restful import Resource, reqparse
import json

class Todo(Resource):
    def get(self, todo):
        todo_list = json.dumps([v for v in todos.find()], default=json_util.default)
        
        if not todo_list:
            return {'response': 'no todo list found'}, 400

        data = json.loads(todo_list)  

        for task in data['todo_name']:
            LOG.info('TODO: %s' % (data['todo_name']))
            LOG.info('TASK: %s' % (task))
            if todo in task:
                return {'response': 'success', 
                        'task': json.dumps(task, default=json_util.default)}, 200

        return {'response': 'Something went terribly wrong'}, 400

    def put(self, todo):
        parser = reqparse.RequestParser()
        parser.add_argument('todo_desc', type=str, required=True, help='Description of task')
        args = parser.parse_args()

        if not todo:
            return {'response': 'no data provided'}, 400
        
        task = {
            "todo_name": todo,
            "todo_desc": args['todo_desc']
        }

        check = todos.find_one(task)
        if check != None:
            return {'response': 'found existing', 
                    'task': json.dumps(check, default=json_util.default)}, 200

        todos.insert(task)

        return {'response': 'success', 'task': json.dumps(task, default=json_util.default)}, 201

class TodoList(Resource):
    def get(self):
        todo_list = [v for v in todos.find()]
        
        if not todo_list:
            return {'response': 'no todo list found'}, 400

        return {'response': 'success', 
                'task': json.dumps(todo_list, default=json_util.default)}, 200
