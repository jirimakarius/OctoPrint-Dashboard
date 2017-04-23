from flask_restful import Resource, marshal_with, fields, reqparse
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Group
from flask import g
from octoprint_dashboard.app import db

access_parser = reqparse.RequestParser()
access_parser.add_argument('access', type=str, help='Access can\'t be converted', location="args")

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')

group_id_parser = reqparse.RequestParser()
group_id_parser.add_argument('groupId', type=int, required=True, help='Group ID can\'t be converted', action='append')


class GroupApi(Resource):
    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        if g.user.superadmin:
            return Group.query.all()
        else:
            if access_parser.parse_args()["access"] == "editable":
                printers = g.user.get_editable_groups()
            else:
                printers = g.user.get_groups()
            return printers

    @superadmin_required
    def post(self):
        args = parser.parse_args()
        group = Group(args["name"])
        db.session.add(group)
        db.session.commit()
        return None, 201, {'Location': "https://localhost:3000/group/{0}".format(group.id)}

    @login_required
    def delete(self):
        args = group_id_parser.parse_args()
        groups = Group.query.filter(Group.id.in_(args["groupId"])).all()
        for group in groups:
            if group.editable(g.user):
                db.session.delete(group)
        db.session.commit()
        return None, 204
