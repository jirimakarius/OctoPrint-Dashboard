from octoprint_dashboard import app, db
from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer, User, Group
from flask import request, g, jsonify
from flask_restful import Resource, marshal_with, fields


class PrinterApi(Resource):
    @login_required
    @marshal_with({
        'name': fields.String
    })
    def get(self):
        if g.user.superadmin:
            pass
            return Printer.query.all()
        else:
            printers=g.user.group[0].printer.all()
            return printers
