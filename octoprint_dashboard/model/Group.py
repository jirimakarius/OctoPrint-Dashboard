from octoprint_dashboard import db
from sqlalchemy.ext.associationproxy import association_proxy


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    user = association_proxy("group_user", "user")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.name
