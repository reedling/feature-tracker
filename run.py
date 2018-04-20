from operator import attrgetter
import os

from flask import render_template, send_from_directory

from app import create_app
from app.models import Feature


flask_app = create_app()

# fake features for now
fake_feature_reqs = [
    Feature(
        title='Buy more hand soap',
        description='Someone used all the hand soap.',
        client='Client A',
        priority=1,
        target_date='05-06-2018',
        product_area='Claims'),
    Feature(
        title='Charge for hand soap',
        description='They can\'t keep getting away with this.',
        client='Client A',
        priority=3,
        target_date='04-06-2018',
        product_area='Billing'),
    Feature(
        title='TPS report',
        description='Thatd be great.',
        client='Client B',
        priority=1,
        target_date='02-05-2018',
        product_area='Reports'),
    Feature(
        title='Simplify soap pipeline',
        description='It is a real hassle to get more hand soap when we run out.',
        client='Client A',
        priority=2,
        target_date='05-06-2018',
        product_area='Policies'),
    Feature(
        title='Make this website',
        description='OMG.',
        client='Client C',
        priority=1,
        target_date='23-04-2018',
        product_area='Claims'),
    Feature(
        title='The HTML/CSS is pretty much good to go!',
        description='Now we need to add KnockoutJS, SQLAlchemy, etc.',
        client='Client C',
        priority=2,
        target_date='23-04-2018',
        product_area='Claims')
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
