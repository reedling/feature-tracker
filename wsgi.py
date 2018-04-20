from app import db
from run import flask_app as application


@application.before_first_request
def initialize():
    with application.app_context():
        db.create_all()


if __name__ == "__main__":
    application.run()
