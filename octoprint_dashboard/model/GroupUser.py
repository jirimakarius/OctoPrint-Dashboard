from octoprint_dashboard.app import db
from octoprint_dashboard.model import User, Group


class GroupUser(db.Model):
    __tablename__ = 'group_user'

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(80), nullable=False, default="user")

    group = db.relationship("Group", backref=db.backref("group_user", lazy="dynamic", cascade='all, delete-orphan'))
    user = db.relationship("User", backref=db.backref("group_user", lazy="dynamic", cascade='all, delete-orphan'))

    def __init__(self, group=None, user=None, role="user"):
        self.group = group
        self.user = user
        self.role = role

    def __repr__(self):
        return '<GroupUser %r>' % self.role
