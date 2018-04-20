from app import db
from run import flask_app as application


with application.app_context():
    db.create_all()
    application.run()
