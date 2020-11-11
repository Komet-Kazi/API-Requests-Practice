# /my_app/__init__.py

from flask import Flask  # import flask

app = Flask(__name__)  # create a instance of Flask object

import my_app.hello.views
