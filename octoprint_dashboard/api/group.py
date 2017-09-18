from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.app import db, socketio
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Group

getGroupParser = reqparse.RequestParser()  # parser for getting groups of user with admin or user role
getGroupParser.add_argument('access', type=str, help='Access can\'t be converted', location="args")

newGroupParser = reqparse.RequestParser()  # parser for new group
newGroupParser.add_argument('name', type=str, required=True, help='Name can\'t be converted')

groupIdParser = reqparse.RequestParser()  # parser multiple group deletion
groupIdParser.add_argument('groupId', type=int, required=True, help='Group ID can\'t be converted', action='append')


class GroupApi(Resource):
    """
    Api class group management
    """

    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        """Gets groups of user with admin or user role according to access parameter"""
        if getGroupParser.parse_args()["access"] == "editable":
            groups = g.user.get_editable_groups()
        else:
            groups = g.user.get_groups()
        return groups

    @superadmin_required
    def post(self):
        """Creates new group"""
        args = newGroupParser.parse_args()
        group = Group(args["name"])
        db.session.add(group)
        db.session.commit()
        return "", 201, {'Location': "https://localhost:3000/group/{0}".format(group.id)}

    @login_required
    def delete(self):
        """Deletes groups by group ids"""
        args = groupIdParser.parse_args()
        groups = g.user.get_editable_groups()
        for group in groups:
            if group.id in args["groupId"]:
                db.session.delete(group)
        db.session.commit()

        socketio.emit("rejoin", broadcast=True, skip_sid=None)
        return "", 204
