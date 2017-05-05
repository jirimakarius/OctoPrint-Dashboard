from sqlalchemy.ext.associationproxy import association_proxy

from octoprint_dashboard.app import db


class User(db.Model):
    """
    Instance of this class equals single record of config in database
    Class behaves like repository of Config records

    User represents human being, logged into app at least once
    """
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
        """
        Creates user with parameters in database or updates access and refresh token of user
        """
        user = User.query.filter_by(username=username).scalar()
        if user is None:
            user = User(username, access_token, refresh_token)
            db.session.add(user)
        else:
            user.access_token = access_token
            user.refresh_token = refresh_token
        db.session.commit()
        return user

    @staticmethod
    def upsert_superadmin(username):
        """
        Makes user superadmin
        """
        user = User.query.filter_by(username=username).scalar()
        if user is None:
            user = User(username, None, None)
            user.superadmin = True
            db.session.add(user)
        else:
            user.superadmin = True
        db.session.commit()

    def get_accessible_printers(self):
        """
        Returns all printers accessible to user with admin role
        """
        from octoprint_dashboard.model import Printer, Group, GroupUser
        if self.superadmin:
            printers = Printer.query.all()
        else:
            printers = Printer.query.join(Printer.group).join(Group.group_user).filter(User.id == self.id,
                                                                                       GroupUser.role == "admin").all()

        return printers

    def get_accessible_printers_id(self, printer_ids):
        """
        Returns printers of given ids accessible to user with admin role
        """
        from octoprint_dashboard.model import Printer, Group, GroupUser
        if self.superadmin:
            printers = Printer.query.filter(Printer.id.in_(printer_ids)).all()
        else:
            printers = Printer.query.filter(Printer.id.in_(printer_ids)) \
                .join(Printer.group).join(Group.group_user) \
                .filter(User.id == self.id, GroupUser.role == "admin").all()

        return printers

    def get_accessible_printer_id(self, printer_id):
        """
        Returns printer of given id accessible to user with admin role or None
        """
        from octoprint_dashboard.model import Printer, Group, GroupUser
        if self.superadmin:
            printer = Printer.query.get(printer_id)
        else:
            printer = Printer.query.filter(Printer.id == printer_id) \
                .join(Printer.group).join(Group.group_user) \
                .filter(User.id == self.id, GroupUser.role == "admin").scalar()

        return printer

    def get_printer_id(self, printer_id):
        """
        Returns printer of given id accessible to user or None
        """
        from octoprint_dashboard.model import Printer, Group
        if self.superadmin:
            printer = Printer.query.get(printer_id)
        else:
            printer = Printer.query.filter(Printer.id == printer_id) \
                .join(Printer.group).join(Group.group_user) \
                .filter(User.id == self.id).scalar()

        return printer

    def get_editable_groups(self):
        """
        Returns groups accessible to user with admin role
        """
        from octoprint_dashboard.model import Group, GroupUser

        if self.superadmin:
            groups = Group.query.all()
        else:
            groups = Group.query.join(Group.group_user).join(GroupUser.user).filter(User.id == self.id).filter(
                GroupUser.role == "admin").all()

        return groups

    def get_editable_group_id(self, id):
        """
        Returns groups of given id accessible to user with admin role
        """
        from octoprint_dashboard.model import Group, GroupUser

        if self.superadmin:
            group = Group.query.get(id)
        else:
            group = Group.query.join(Group.group_user).join(GroupUser.user).filter(User.id == self.id).filter(
                GroupUser.role == "admin").filter(Group.id == id).scalar()

        return group

    def get_groups(self):
        """
        Returns groups accessible to user
        """
        from octoprint_dashboard.model import Group, GroupUser

        if self.superadmin:
            groups = Group.query.all()
        else:
            groups = Group.query.join(Group.group_user).join(GroupUser.user).filter(User.id == self.id).all()

        return groups
