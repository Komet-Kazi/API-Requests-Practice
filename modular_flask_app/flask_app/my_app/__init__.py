# /my_app/__init__.py

from flask import Flask  # import flask
from my_app.hello.views import hello  # import our blueprint 'hello'


app = Flask(__name__)  # create a instance of Flask object

# register the blueprint on the application object.
app.register_blueprint(hello)
