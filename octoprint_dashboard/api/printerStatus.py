import requests
from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

printerControlParser = reqparse.RequestParser()
printerControlParser.add_argument('printerId', type=int, required=True, help='Printer ID can\'t be converted',
                                  action='append')
printerControlParser.add_argument('bed', type=int, help='Bed temperature can\'t be converted')
printerControlParser.add_argument('tool', type=int, help='Tool temperature can\'t be converted')
printerControlParser.add_argument('pause', type=bool, help='Pause can\'t be converted')
printerControlParser.add_argument('cancel', type=bool, help='Cancel can\'t be converted')


class PrinterStatusApi(Resource):
    @login_required
    @marshal_with({
        'state': fields.Nested({
            'temperature': fields.Nested({
                'bed': fields.Nested({
                    'actual': fields.Integer,
                    'target': fields.Integer
                }),
                'tool': fields.Nested({
                    'actual': fields.Integer,
                    'target': fields.Integer
                }, attribute="tool0")
            }),
            'state': fields.String(attribute="state.text"),
            'job': fields.Nested({
                'printTimeLeft': fields.Integer(attribute='progress.printTimeLeft'),
                'completion': fields.Float(attribute='progress.completion'),
                'fileName': fields.String(attribute='file.name')
            })
        }),
        'id': fields.Integer,
        'name': fields.String,
        'group': fields.List(
            fields.Nested({
                'name': fields.String
            })
        )
    })
    def get(self):
        printers = g.user.get_accessible_printers()
        states = [x.set_state(Printer.states.get(x.id)) for x in printers]
        return states, 200

    @login_required
    def post(self):
        args = printerControlParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        for printer in printers:
            try:
                if args["bed"] is not None:
                    OctoprintService.set_bed_temperature(printer, args["bed"])
                if args["tool"] is not None:
                    OctoprintService.set_tool_temperature(printer, args["tool"])
                if args["pause"] is not None:
                    OctoprintService.pause(printer)
                if args["cancel"] is not None:
                    OctoprintService.cancel(printer)
            except (requests.ConnectionError, RuntimeError):
                pass
        return "", 200
