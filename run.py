from operator import attrgetter
import os

from flask import (flash, redirect, render_template, request,
                   send_from_directory, url_for)
from sqlalchemy import exc

from app import create_app, db
from app.models import Feature


flask_app = create_app('prod')


@flask_app.route('/')
def index():
    features = []
    try:
        features = Feature.query.all()
    except exc.ProgrammingError:
        print('No features to display yet')
    return render_template('index.html',
                           feature_reqs=sorted(
                               features,
                               key=attrgetter('priority', 'due_stamp', 'title')
                           ))


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
    return redirect(url_for('index'))


@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
