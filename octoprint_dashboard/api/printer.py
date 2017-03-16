from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse
import requests

from octoprint_dashboard import db
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
parser.add_argument('apikey', type=str, required=True, help='Apikey can\'t be converted')
parser.add_argument('ip', type=str, required=True, help='ip can\'t be converted')


class PrinterApi(Resource):
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

    # @superadmin_required
    def post(self):
        args = parser.parse_args()

        try:
            response = OctoprintService.get_version(args['apikey'], args['ip'])
        except requests.exceptions.ConnectionError:
            return "Bad IP given, expected format: [localhost:3200]", 400
        if response.status_code==401:
            return "Unaccessible printer", 400

        printer = Printer(args["name"], args["apikey"], args['ip'])
        db.session.add(printer)
        db.session.commit()
        return None, 201, {'Location': "https://localhost:3000/printer/{0}".format(printer.id)}
