from app import db
from run import flask_app as application


if __name__ == "__main__":
    with application.app_context():
        db.create_all()
        application.run()
