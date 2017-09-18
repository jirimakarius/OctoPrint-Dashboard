from flask import g, request
from flask_restful import Resource, marshal_with, fields

from octoprint_dashboard.app import db, socketio
from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer, User, GroupUser


class GroupSettingsApi(Resource):
    """
    Api class for single group settings
    """

    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String,
        'printers': fields.List(
            fields.Nested({
                "id": fields.Integer,
                "name": fields.String
            }),
            attribute="printer"
        ),
        'users': fields.List(
            fields.Nested({
                "id": fields.Integer(attribute="user.id"),
                "username": fields.String(attribute="user.username"),
                "role": fields.String
            }),
            attribute="group_user"
        )
    })
    def get(self, group_id):
        """Gets settings of group"""
        group = g.user.get_editable_group_id(group_id)
        if group:
            return group, 200

        return "Missing right for group", 403

    @login_required
    def put(self, group_id):
        """Modifies settings of group"""
        group = g.user.get_editable_group_id(group_id)
        if not group:
            return "Missing right for group", 403

        args = request.json
        group.name = args["name"]
        printer_ids = [x["id"] for x in args["printers"]]
        printers = Printer.query.filter(
            Printer.id.in_(printer_ids)) if printer_ids else []  # associate group with printers in request
        group.printer = printers

        usernames = [x["username"] for x in args["users"]]
        users = User.query.filter(User.username.in_(usernames)).all() if usernames else []
        group.group_user = []
        for input in args["users"]:  # associate group with users trough class GroupUser in request, creating new
            # users in database
            found = None
            for user in users:
                if user.username == input["username"]:
                    found = user
            if found is None:
                found = User(input["username"])
            group.group_user.append(GroupUser(group, found, input["role"]))

        db.session.commit()

        socketio.emit("rejoin", broadcast=True, skip_sid=None)
        return "", 200
