from octoprint_dashboard import db
from sqlalchemy.ext.associationproxy import association_proxy

from octoprint_dashboard.model import User

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    user = association_proxy("group_user", "user")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Group %r>' % self.name

    def editable(self, user: User):
        from octoprint_dashboard.model import GroupUser
        if user.superadmin:
            return True

        role = GroupUser.query.join(User).join(Group).filter(User.id == user.id, Group.id == self.id).scalar().role
        if role == 'admin':
            return True

        return False
