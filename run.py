from datetime import datetime
from operator import attrgetter
import os

from flask import (flash, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)
from sqlalchemy import cast, exc, Integer

from app import create_app, db
from app.models import Feature

flask_app = create_app(os.environ['ENV'] if 'ENV' in os.environ else 'dev')


# Routes #


@flask_app.before_first_request
def initialize():
    with flask_app.app_context():
        db.create_all()


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/requests')
def requests():
    features = get_all_requests()
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


@flask_app.route('/request-counts')
def request_counts():
    return jsonify(get_request_counts_by_client())


@flask_app.route('/view-request')
def view_request_no_param():
    return redirect(url_for('index'))


@flask_app.route('/view-request/<feature_id>')
def view_request(feature_id):
    f = get_request_by_id(feature_id)
    if f is None:
        flash('No feature request found with that id: {}'.format(feature_id),
              'warning')
        return redirect(url_for('index'))
    else:
        return render_template('view_request.html', feature=f)


@flask_app.route('/new-request')
def new_request():
    return render_template('new_request.html')


@flask_app.route('/submit-request', methods=['GET', 'POST'])
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
        message, failed = increment_priorities_to_make_room(new_feature)
        flash(message, 'error' if failed else 'message')
    return redirect(url_for('index'))


@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Helpers #


def get_all_requests():
    features = []
    try:
        features = Feature.query.all()
    except exc.ProgrammingError:
        print('No features to display yet')
    return features


def get_request_by_id(request_id):
    return Feature.query.filter_by(id=request_id).first()


def get_request_counts_by_client():
    counts = {}
    for f in get_all_requests():
        if f.client not in counts:
            counts[f.client] = 0
        counts[f.client] += 1
    return counts


def increment_priorities_to_make_room(new_f):
    to_increment = Feature.query.filter(
        Feature.client == new_f.client,
        Feature.priority >= new_f.priority
    ).all()
    for f in to_increment:
        f.priority = str(int(f.priority) + 1)
    db.session.add(new_f)
    try:
        db.session.commit()
        message = 'Feature request submitted.'
        incremented = len(to_increment)
        if incremented > 0:
            message += '  (Incremented priorit{} for {} other{}.)'.format(
                'ies' if incremented > 1 else 'y',
                incremented,
                's' if incremented > 1 else ''
            )
        return message, False
    except exc.IntegrityError as ie:
        print(ie)
        return 'Failed to submit feature request.', True
    except exc.DataError as de:
        print(de)
        return 'Invalid data submitted for feature request.', True
