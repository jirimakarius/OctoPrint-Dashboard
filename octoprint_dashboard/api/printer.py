from flask import g, request
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.app import db, socketio
from octoprint_dashboard.login import login_required, superadmin_required
from octoprint_dashboard.model import Printer, Config
from octoprint_dashboard.services import OctoprintService

newPrinterParser = reqparse.RequestParser()  # parser for printer adding or validation
newPrinterParser.add_argument('validate', type=bool, location="args")

validateParser = reqparse.RequestParser()  # parser for printer validation
validateParser.add_argument('name', type=str, required=True, help='Name required')
validateParser.add_argument('apikey', type=str, required=True, help='Apikey required')
validateParser.add_argument('ip', type=str, required=True, help='IP required')

printerIdParser = reqparse.RequestParser()  # parser for printer ids
printerIdParser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


class PrinterApi(Resource):
    """
    Api class for printer management
    """

    @login_required
    @marshal_with({
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        """Gets printers of groups with admin rights"""
        return g.user.get_accessible_printers(), 200

    @superadmin_required
    def post(self):
        """Creates or validates printer"""
        args = newPrinterParser.parse_args()
        if args["validate"]:  # validation of printers access data
            args = validateParser.parse_args()
            url = "http://{0}".format(args['ip'])
            auth = OctoprintService.auth(args['apikey'], url)
            if auth is not None:
                return auth, 400
            return "", 200

        else:  # creates multiple printers
            from octoprint_dashboard.app import octoprint_status
            body = request.json
            for args in body:
                url = "http://{0}".format(args['ip'])
                auth = OctoprintService.auth(args['apikey'], url)
                if auth is not None:
                    continue
                printer = Printer(args["name"], args["apikey"], url)
                db.session.add(printer)
                db.session.commit()
                octoprint_status.add_listener(printer)

            socketio.emit("rejoin", broadcast=True, skip_sid=None)
            return "", 201

    @superadmin_required
    def delete(self):
        """Deletes printer according to given printer ids"""
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        for printer in printers:
            db.session.delete(printer)
        db.session.commit()
        for printer_id in args["printerId"]:
            socketio.close_room(str(printer_id))

        socketio.emit("rejoin", broadcast=True, skip_sid=None)
        return "", 204


class PrinterIdApi(Resource):
    """
    Api class for single printer management
    """

    @superadmin_required
    def put(self, printer_id):
        """Changes printer access data or name"""
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

        socketio.emit("rejoin", broadcast=True, skip_sid=None)
        return "", 200
