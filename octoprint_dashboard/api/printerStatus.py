from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
parser.add_argument('apikey', type=str, required=True, help='Apikey can\'t be converted')
parser.add_argument('ip', type=str, required=True, help='ip can\'t be converted')


class PrinterStatusIdApi(Resource):
    @login_required
    @marshal_with({
        'temperature': fields.Nested({
            'bed': fields.Integer(attribute="bed.actual"),
            'tool': fields.Integer(attribute="tool0.actual")
        }),
        'state': fields.String(attribute="state.text")
    })
    def get(self, printer_id):
        state = Printer.states.get(printer_id)
        return state, 200


class PrinterStatusApi(Resource):
    @login_required
    @marshal_with({
        'temperature': fields.Nested({
            'bed': fields.Integer(attribute="bed.actual"),
            'tool': fields.Integer(attribute="tool0.actual")
        }),
        'state': fields.String(attribute="state.text")
    })
    def get(self):
        printers = g.user.get_accessible_printers()
        states = [Printer.states.get(x.id) for x in printers]
        return states, 200
