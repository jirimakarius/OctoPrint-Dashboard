from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
parser.add_argument('apikey', type=str, required=True, help='Apikey can\'t be converted')
parser.add_argument('ip', type=str, required=True, help='ip can\'t be converted')


class PrinterStatusApi(Resource):
    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        if g.user.superadmin:
            return Printer.query.all()
        else:
            printers = g.user.get_accessible_printers()
            return printers
