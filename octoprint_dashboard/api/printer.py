from flask import g, request
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.app import db, scheduler
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Printer, Config
from octoprint_dashboard.services import OctoprintService

newPrinterParser = reqparse.RequestParser()
newPrinterParser.add_argument('validate', type=bool, location="args")

validateParser = reqparse.RequestParser()
validateParser.add_argument('name', type=str, required=True, help='Name required')
validateParser.add_argument('apikey', type=str, required=True, help='Apikey required')
validateParser.add_argument('ip', type=str, required=True, help='IP required')

printerIdParser = reqparse.RequestParser()
printerIdParser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


class PrinterApi(Resource):
    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        return g.user.get_accessible_printers(), 200

    @superadmin_required
    def post(self):
        args = newPrinterParser.parse_args()
        if args["validate"]:
            args = validateParser.parse_args()
            url = "http://{0}".format(args['ip'])
            auth = OctoprintService.auth(args['apikey'], url)
            if auth is not None:
                return auth, 400
            return "", 200

        else:
            body = request.json
            config = Config.query.first()
            for args in body:
                url = "http://{0}".format(args['ip'])
                auth = OctoprintService.auth(args['apikey'], url)
                if auth is not None:
                    continue
                printer = Printer(args["name"], args["apikey"], url)
                db.session.add(printer)
                db.session.commit()
                scheduler.add_printer_status_job(printer, config.server_refresh)
            return "", 201

    @superadmin_required
    def delete(self):
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        for printer in printers:
            db.session.delete(printer)
        db.session.commit()
        scheduler.remove_printer_status_job(args["printerId"])
        return "", 204


class PrinterIdApi(Resource):
    @superadmin_required
    def put(self, printer_id):
        args = validateParser.parse_args()
        url = "http://{0}".format(args['ip'])
        auth = OctoprintService.auth(args['apikey'], url)
        if auth is not None:
            return "", 400
        printer = Printer.query.get(printer_id)
        printer.name = args['name']
        printer.apikey = args['apikey']
        printer.url = url
        db.session.commit()
        config = Config.query.first()
        scheduler.remove_printer_status_job([printer_id])
        scheduler.add_printer_status_job(printer, config.server_refresh)
        return "", 200
