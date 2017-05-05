from sqlalchemy.ext.associationproxy import association_proxy

from octoprint_dashboard.app import db
from octoprint_dashboard.model import User


class Group(db.Model):
    """
    Instance of this class equals single record of config in database
    Class behaves like repository of Config records

    Group represent link between users and printers, single group has
    M:N users and M:N printers
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    user = association_proxy("group_user", "user")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.name

    def editable(self, user: User):
        """Returns true if group is editable by given user else false"""
        from octoprint_dashboard.model import GroupUser
        if user.superadmin:
            return True

        role = GroupUser.query.join(User).join(Group).filter(User.id == user.id, Group.id == self.id).scalar().role
        if role == 'admin':
            return True

        return False
