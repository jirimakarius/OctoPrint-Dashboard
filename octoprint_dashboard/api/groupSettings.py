from flask import g
from flask_restful import Resource, marshal_with, fields

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Group


class GroupSettingsApi(Resource):
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
        group = Group.query.get(group_id)
        if group.editable(g.user):
            return group, 200

        return "Missing right for group", 403
