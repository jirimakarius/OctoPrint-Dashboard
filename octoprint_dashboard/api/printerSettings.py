import requests
from flask import g, request
from flask_restful import Resource, marshal_with, fields, reqparse

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


class PrinterSettingsApi(Resource):
    @login_required
    def get(self):
        args = parser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        settings = []
        for printer in printers:
            try:
                ret = OctoprintService.get_settings(printer).json()
                ret["printerId"] = printer.id
                settings.append(ret)
            except requests.ConnectionError:
                pass
        return settings, 200

    @login_required
    def post(self):
        args = parser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])

        for printer in printers:
            try:
                ret = OctoprintService.save_settings(printer, request.json)
            except requests.ConnectionError:
                pass

        return None, 202
