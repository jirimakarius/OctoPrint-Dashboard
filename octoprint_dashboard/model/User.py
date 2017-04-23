from octoprint_dashboard.app import db
from sqlalchemy.ext.associationproxy import association_proxy


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
        from octoprint_dashboard.model import Group, GroupUser

        user = User.query.filter_by(username=username).scalar()
        if user is None:
            user = User(username, access_token, refresh_token)
            user.group_user.append(GroupUser(group=Group("default"), user=user))
            db.session.add(user)
        else:
            user.access_token = access_token
            user.refresh_token = refresh_token
        db.session.commit()
        return user

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

    def get_accessible_printers(self):
        from octoprint_dashboard.model import Printer, Group, GroupUser
        if self.superadmin:
            printers = Printer.query.all()
        else:
            printers = Printer.query.join(Printer.group).join(Group.group_user).filter(User.id == self.id, GroupUser.role == "admin").all()

        return printers

    def get_accessible_printers_id(self, printer_ids):
        from octoprint_dashboard.model import Printer, Group, GroupUser
        if self.superadmin:
            printers = Printer.query.filter(Printer.id.in_(printer_ids)).all()

        else:
            printers = Printer.query.filter(Printer.id.in_(printer_ids))\
                .join(Printer.group).join(Group.group_user)\
                .filter(User.id == self.id, GroupUser.role == "admin").all()

        return printers

    def get_editable_groups(self):
        from octoprint_dashboard.model import Group, GroupUser
        groups = Group.query.join(Group.group_user).join(GroupUser.user).filter(User.id == self.id).filter(GroupUser.role == "admin").all()

        return groups

    def get_groups(self):
        from octoprint_dashboard.model import Group, GroupUser
        groups = Group.query.join(Group.group_user).join(GroupUser.user).filter(User.id == self.id).all()

        return groups
