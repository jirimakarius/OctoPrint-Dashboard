from flask_restful import Resource, marshal_with, fields, reqparse
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Group
from flask import g
from octoprint_dashboard import db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')


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
            printers = g.user.get_editable_groups()
            return printers

    # @superadmin_required
    def post(self):
        args = parser.parse_args()
        group = Group(args["name"])
        db.session.add(group)
        db.session.commit()
        return None, 201, {'Location': "https://localhost:3000/group/{0}".format(group.id)}