from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
parser.add_argument('apikey', type=str, required=True, help='Apikey can\'t be converted')
parser.add_argument('ip', type=str, required=True, help='ip can\'t be converted')


class PrinterStatusApi(Resource):
    # @login_required
    @marshal_with({
        'temperature': fields.Nested({
            'bed': fields.Integer,
            'tool': fields.Integer
        }),
        'state': fields.String
    })
    def get(self, printer_id):
        # printer = Printer.query.get(printer_id)
        state = Printer.states.get(printer_id)
        print(state)
        # state = Printer.states[printer_id]
        # response = OctoprintService.get_printer_state(printer)
        # print(response.text)
        # print(response.status_code)
        return state, 200

