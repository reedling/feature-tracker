from datetime import datetime


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
        return datetime.strptime(self.due, '%d-%m-%Y').timestamp()

    def __str__(self):
        return '{} -- {}'.format(self.title, self.client)
