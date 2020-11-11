# /my_app/hello/views.py - Fetch the mssage corresponding to the key that is asked for and also can create or update a message

from my_app import app
from my_app.hello.models import MESSAGES
from flask import render_template, request

@app.route('/')  # http://127.0.0.1:5000/
@app.route('/hello')  # http://127.0.0.1:5000/hello
def hello_world():
    '''The argument passed in the URL is fetched from the request object using 'request.args.get('user')'
    If the URL has the query argument: 'user', use the value supplied. >> http://127.0.0.1:5000/hello?user=John.
    if no 'user' argument was passed in the URL, we use the default argument, 'Shalabh'. >> http://127.0.0.1:5000/hello.
    Then, this value is passed to the context of the template to be rendered: 'index.html'
    The resulting template is rendered.
    '''
    user = request.args.get('user', 'Shalabh')
    return render_template('index.html', user=user)

@app.route('/show/<key>')  # http://127.0.0.1:5000/show/default
def get_message(key):
    '''View a message after providing its key via the above Url route
    if the key provided is not found display message saying so'''
    return MESSAGES.get(key) or f'{key} not found!'

@app.route('/add/<key>/<message>')  # http://127.0.0.1:5000/add/great/Flask%20is%20great!!
def add_or_update_message(key, message):
    '''add or update a key,value to MESSAGES via the above Url route'''
    MESSAGES[key] = message
    return f'{key} has been Added//Updated!'
