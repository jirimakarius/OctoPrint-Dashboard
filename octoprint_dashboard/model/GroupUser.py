from octoprint_dashboard.app import db


class GroupUser(db.Model):
    """
    Instance of this class equals single record of config in database
    Class behaves like repository of Config records

    GroupUser represents link between Groups and Users.
    This class is used because every relation has role attribute
    """
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
