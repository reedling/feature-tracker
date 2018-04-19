from operator import attrgetter
import os

from flask import render_template, send_from_directory

from app import create_app
from app.models import Feature


flask_app = create_app()

# fake features for now
fake_feature_reqs = [
    Feature('Buy more hand soap', 'Someone used all the hand soap.', 'Client A', 1, '05-06-2018', 'Claims'),
    Feature('Charge for hand soap', 'They can\'t keep getting away with this.', 'Client A', 3, '04-06-2018', 'Billing'),
    Feature('TPS report', 'Thatd be great.', 'Client B', 1, '02-05-2018', 'Reports'),
    Feature('Simplify soap pipeline', 'It is a real hassle to get more hand soap when we run out.', 'Client A', 2, '05-06-2018', 'Policies'),
    Feature('Make this website', 'OMG.', 'Client C', 1, '23-04-2018', 'Claims'),
    Feature('The HTML/CSS is pretty much good to go!', 'Now we need to add KnockoutJS, SQLAlchemy, etc.', 'Client C', 2, '23-04-2018', 'Claims')
]


@flask_app.route('/')
def index():
    return render_template('index.html',
                           feature_reqs=sorted(
                               fake_feature_reqs,
                               key=attrgetter('priority', 'due_stamp', 'title')
                           ))


@flask_app.route('/new-request')
def new_request():
    return render_template('new_request.html')


@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
