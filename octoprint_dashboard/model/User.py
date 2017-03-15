from octoprint_dashboard import db
from sqlalchemy.ext.associationproxy import association_proxy
from octoprint_dashboard.model import Group, GroupUser


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    access_token = db.Column(db.String(80))
    refresh_token = db.Column(db.String(80))
    superadmin = db.Column(db.Boolean, default=False)

    group = association_proxy("group_user", "group")

    def __init__(self, username=None, access_token=None, refresh_token=None):
        self.username = username
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def upsert(username, access_token, refresh_token):
        user = User.query.filter_by(username=username).scalar()
        if user is None:
            user = User(username, access_token, refresh_token)
            user["group_user"].append(GroupUser(Group("default"), user))
            db.session.add()
        else:
            user.access_token = access_token
            user.refresh_token = refresh_token
        db.session.commit()

    @staticmethod
    def upsert_superadmin(username):
        user = User.query.filter_by(username=username).scalar()
        if user is None:
            user = User(username, None, None)
            user.superadmin = True
            db.session.add(user)
        else:
            user.superadmin = True
        db.session.commit()