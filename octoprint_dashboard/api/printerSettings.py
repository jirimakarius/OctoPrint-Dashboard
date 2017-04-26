import requests
from flask import g, request
from flask_restful import Resource, reqparse, marshal_with, fields

from octoprint_dashboard.login import login_required
from octoprint_dashboard.services import OctoprintService

printerIdParser = reqparse.RequestParser()
printerIdParser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


class PrinterSettingsApi(Resource):
    @login_required
    @marshal_with({
        "temperature": fields.Nested({
            "profiles": fields.List(
                fields.Nested({
                    "bed": fields.String,
                    "extruder": fields.String,
                    "name": fields.String
                })
            )
        })
    })
    def get(self):
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        settings = []
        for printer in printers:
            try:
                ret = OctoprintService.get_settings(printer)
                ret["printerId"] = printer.id
                settings.append(ret)
            except (requests.ConnectionError, RuntimeError):
                pass
        return settings, 200

    @login_required
    def post(self):
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])

        for printer in printers:
            try:
                ret = OctoprintService.save_settings(printer, request.json)
            except (requests.ConnectionError, RuntimeError):
                pass

        return "", 200
