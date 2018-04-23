## Feature Tracker
(This demo was built as a take-home project.)

The app displays a board of feature requests, sorted by urgency.\
Users can submit new feature requests or view the details of those that already exist.

It was built using Flask, KnockoutJS, and SQL Alchemy.

The following features were beyond the scope of the project, but they'd be good next steps:
* Improved accessibility
* Authentication
* Deleting/editing features
* Pagination of feature requests
* Options for sorting items on the feature board
* Cosmetic options for coloring features by urgency, by client, etc.

## Installation
The app is [hosted on Heroku here](https://feature-tracker-demo.herokuapp.com/) if you just want to try it out.

To run locally, you'll want [pipenv](https://docs.pipenv.org/) and [PostgreSQL](https://www.postgresql.org/download/):
```
git clone https://github.com/reedling/feature-tracker.git
cd feature-tracker
pipenv install -r requirements.txt
```

Next, make your PostgreSQL db URI available as an environment variable:
```
export DATABASE_URL="postgresql://reedling@localhost/reedling"
```
Or just hardcode it in the config file at config/dev.py:
```
SQLALCHEMY_DATABASE_URI = 'postgresql://reedling@localhost/reedling'
```

Finally, run:
```
pipenv run python wsgi.py
```