from flask import g, request
from flask_restful import Resource, marshal_with, fields, reqparse
import requests

from octoprint_dashboard.app import db, scheduler
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('validate', type=bool, location="args")

validateParser = reqparse.RequestParser()
validateParser.add_argument('name', type=str, required=True, help='Name required')
validateParser.add_argument('apikey', type=str, required=True, help='Apikey required')
validateParser.add_argument('ip', type=str, required=True, help='IP required')


printer_id_parser = reqparse.RequestParser()
printer_id_parser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


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

    @superadmin_required
    def post(self):
        args = parser.parse_args()
        if args["validate"]:
            args = validateParser.parse_args()
            url = "http://{0}".format(args['ip'])
            auth = OctoprintService.auth(args['apikey'], url)
            if auth is not None:
                return auth, 400
            return None, 200

        else:
            body = request.json
            for args in body:
                url = "http://{0}".format(args['ip'])
                auth = OctoprintService.auth(args['apikey'], url)
                if auth is not None:
                    continue
                printer = Printer(args["name"], args["apikey"], url)
                db.session.add(printer)
                db.session.commit()
                scheduler.add_printer_status_job(printer, 5)
            return None, 201

    @superadmin_required
    def delete(self):
        args = printer_id_parser.parse_args()
        printers = Printer.query.filter(Printer.id.in_(args["printerId"])).all()
        for printer in printers:
            db.session.delete(printer)
        db.session.commit()
        scheduler.remove_printer_status_job(args["printerId"])
        return None, 204
