from octoprint_dashboard import app, db
from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer, User, Group
from flask import request, g, jsonify
from flask_restful import Resource, marshal_with, fields


class PrinterApi(Resource):
    @login_required
    @marshal_with({
        'username': fields.String,
        'group_user': fields.Nested({
            'role': fields.String
        })
    })
    def get(self):
        if g.user.superadmin:
            return Printer.query.all()
        else:
            username = g.user
            # user=User.query.join(Group).filter_by(username=username).scalar()
            print(username.group_user)
            return username
