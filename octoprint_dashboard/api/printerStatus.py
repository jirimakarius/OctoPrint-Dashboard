from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')
parser.add_argument('bed', type=int, help='Bed temperature can\'t be converted')
parser.add_argument('tool', type=int, help='Tool temperature can\'t be converted')


class PrinterStatusIdApi(Resource):
    @login_required
    @marshal_with({
        'temperature': fields.Nested({
            'bed': fields.Integer(attribute="bed.actual"),
            'tool': fields.Integer(attribute="tool0.actual")
        }),
        'state': fields.String(attribute="state.text"),
        'job': fields.Nested({
            'printTime': fields.Integer(attribute='lastPrintTime'),
            'fileName': fields.String(attribute='file.name')
        })
    })
    def get(self, printer_id):
        state = Printer.states.get(printer_id)
        return state, 200


class PrinterStatusApi(Resource):
    @login_required
    @marshal_with({
        'state': fields.Nested({
            'temperature': fields.Nested({
                'bed': fields.Integer(attribute="bed.actual"),
                'tool': fields.Integer(attribute="tool0.actual")
            }),
            'state': fields.String(attribute="state.text"),
            'job': fields.Nested({
                'printTime': fields.Integer(attribute='lastPrintTime'),
                'fileName': fields.String(attribute='file.name')
            })
        }),
        'id': fields.Integer,
        'name': fields.String
    })
    def get(self):
        printers = g.user.get_accessible_printers()
        states = [x.setState(Printer.states.get(x.id)) for x in printers]
        # print(states)
        return states, 200

    def post(self):
        args = parser.parse_args()
        printers = Printer.query.filter(Printer.id.in_(args["printerId"])).all()

        for printer in printers:
            if args["bed"]:
                OctoprintService.set_bed_temperature(printer, args["bed"])
            if args["tool"]:
                OctoprintService.set_tool_temperature(printer, args["tool"])

        return None, 200
