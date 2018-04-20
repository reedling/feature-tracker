from operator import attrgetter
import os

from flask import (flash, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)
from sqlalchemy import exc

from app import create_app, db
from app.models import Feature

flask_app = create_app(os.environ['ENV'] if 'ENV' in os.environ else 'dev')


@flask_app.before_first_request
def initialize():
    with flask_app.app_context():
        db.create_all()


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/requests')
def all_requests():
    features = []
    try:
        features = Feature.query.all()
    except exc.ProgrammingError:
        print('No features to display yet')
    return jsonify([{
        "title": f.title,
        "desc": f.description,
        "client": f.client,
        "priority": f.priority,
        "target_date": f.target_date,
        "area": f.product_area,
        "id": f.id
    } for f in sorted(features,
                      key=attrgetter('priority', 'due_stamp', 'title')
                      )])


@flask_app.route('/new-request')
def new_request():
    return render_template('new_request.html')


@flask_app.route('/submit-request', methods=['POST'])
def submit_request():
    if request.method == 'POST':
        new_feature = Feature(
            title=request.form['title'],
            description=request.form['desc'],
            client=request.form['client'],
            priority=request.form['priority'],
            target_date=request.form['target'],
            product_area=request.form['area']
        )
        db.session.add(new_feature)
        try:
            db.session.commit()
            flash('Feature request submitted.\nThanks for your input!')
        except exc.IntegrityError:
            flash('Failed to submit feature request.', 'error')
        except exc.DataError:
            flash('Invalid data submitted for feature request.', 'error')
    return redirect(url_for('index'))


@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
