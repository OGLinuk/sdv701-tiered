from app import app, LOG
from flask import render_template, request, redirect
import json
import requests

@app.route('/todos', methods=['GET', 'POST'])
def serve_todos():
    LOG.info('serve_todos')
    
    todo_list = requests.get('http://tiered-backend:9124/todo').json()
    
    if not todo_list:
        return render_template('/todo.html', todo='No todo list found')
    
    return render_template('/todo.html', todo=json.loads(todo_list['task']))

@app.route('/upload', methods=['GET', 'POST'])
def serve_upload_todo():
    if request.method == 'POST':
        LOG.info('serve_todo(POST)')

        name = request.values.get('todo_name')
        desc = request.values.get('todo_desc')

        r = requests.put('http://tiered-backend:9124/todo/%s' % (name), data={"todo_desc": desc})
        
        LOG.info("Req.put response: %s" % (r.status_code))

        return redirect('/todos')

    if request.method == 'GET':
        LOG.info('serve_upload_todo(GET)')
        return render_template('/upload.html')