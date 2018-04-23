import os

DEBUG = True
SECRET_KEY = 'secretTestingKeyThatHopefullyNoOneWillGuess'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
