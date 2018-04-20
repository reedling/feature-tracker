from datetime import datetime

from app import db


class Feature(db.Model):
    __tablename__ = 'feature'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    client = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.String(10))
    product_area = db.Column(db.String(8), nullable=False)

    @property
    def due_stamp(self):
        return datetime.strptime(self.target_date, '%d-%m-%Y').timestamp()

    def __str__(self):
        return '{} -- {}'.format(self.title, self.client)
