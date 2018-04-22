from datetime import datetime

from app import db


class Feature(db.Model):
    __tablename__ = 'feature'

    # # Originally planned to use a unique constraint to ensure client-priority
    # # combos were unique, but it's not necessary.
    # __table_args__ = (
    #     db.UniqueConstraint('client', 'priority', name='_client_priority_uc'),
    # )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    client = db.Column(db.String(8), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.String(10), nullable=False)
    product_area = db.Column(db.String(8), nullable=False)

    @property
    def due_stamp(self):
        return datetime.strptime(self.target_date, '%Y-%m-%d').timestamp()

    def __str__(self):
        return '{} -- {}'.format(self.title, self.client)
