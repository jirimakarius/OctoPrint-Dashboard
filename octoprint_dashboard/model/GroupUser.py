from octoprint_dashboard import db
from .User import User
from .Group import Group


class GroupUser(db.Model):
    __tablename__ = 'group_user'

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(80), nullable=False, default="user")

    group = db.relationship(Group, backref="group_user")
    user = db.relationship(User, backref="group_user")

    def __init__(self, group=None, user=None, role="user"):
        self.group = group
        self.user = user
        self.role = role

    def __repr__(self):
        return '<GroupUser %r>' % self.role
