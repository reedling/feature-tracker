import datetime
from operator import attrgetter
import os

from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

epoch = datetime.datetime.utcfromtimestamp(0)


class Feature:
    def __init__(self, title, desc, client, pri, due, area):
        self.title = title
        self.description = desc
        self.client = client
        self.priority = pri
        self.due = due
        self.product_area = area

    @property
    def due_stamp(self):
        return datetime.datetime.strptime(self.due, '%d-%m-%Y').timestamp()

    def __str__(self):
        return '{} -- {}'.format(self.title, self.client)


fake_feature_reqs = [
    Feature('Buy more hand soap', 'Someone used all the hand soap.', 'Client A', 1, '05-06-2018', 'Claims'),
    Feature('Charge for hand soap', 'They can\'t keep getting away with this.', 'Client A', 3, '04-06-2018', 'Billing'),
    Feature('TPS report', 'Thatd be great.', 'Client B', 1, '02-05-2018', 'Reports'),
    Feature('Simplify soap pipeline', 'It is a real hassle to get more hand soap when we run out.', 'Client A', 2, '05-06-2018', 'Policies'),
    Feature('Make this website', 'OMG.', 'Client C', 1, '23-04-2018', 'Claims'),
    Feature('The HTML/CSS is pretty much good to go!', 'Now we need to add KnockoutJS, SQLAlchemy, etc.', 'Client C', 2, '23-04-2018', 'Claims')
]


@app.route('/')
def index():
    return render_template('index.html',
                           feature_reqs=sorted(
                               fake_feature_reqs,
                               key=attrgetter('priority', 'due_stamp', 'title')
                           ))


@app.route('/new-request')
def new_request():
    return render_template('new_request.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
