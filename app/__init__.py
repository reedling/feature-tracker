# app/__init__.py
import os

from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(env='dev'):
    flask_app = Flask(__name__)
    config = os.path.join(os.getcwd(), 'config', env + '.py')
    flask_app.config.from_pyfile(config)
    db.init_app(flask_app)
    bootstrap.init_app(flask_app)

    return flask_app
