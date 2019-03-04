from app import app, LOG, todos
from flask import render_template, request, redirect

@app.route('/todo', methods=['GET', 'POST'])
def serve_todo():
    LOG.info('serve_todo')
    
    todo = [v for v in todos.find()]
    
    if len(todo) < 1:
        return render_template('/todo.html', len=0, todo=None)
    
    return render_template('/todo.html', len=len(todo), todo=todo)

@app.route('/upload', methods=['GET', 'POST'])
def serve_upload_todo():
    if request.method == 'POST':
        LOG.info('serve_todo(POST)')

        todo = {
            "name": request.values.get('todo_name'),
            "desc": request.values.get('todo_desc')
        }

        check = todos.find_one(todo)
        if check != None:
            return redirect('/todo')

        todos.insert(todo)

        return redirect('/todo')

    if request.method == 'GET':
        LOG.info('serve_upload_todo(GET)')
        return render_template('/upload.html')