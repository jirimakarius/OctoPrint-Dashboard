from urllib import parse as urlparse

import requests
from flask import g, request
from flask_restful import Resource, reqparse, fields

from octoprint_dashboard.app import socketio
from octoprint_dashboard.login import login_required
from octoprint_dashboard.services import OctoprintService
from .decorators import selective_marshal_with

printerIdParser = reqparse.RequestParser()  # parser for printer ids in query
printerIdParser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')


class PrinterSettingsApi(Resource):
    """
    Api class for OctoPrints settings of printer
    """

    class ParsedUrl(fields.Raw):
        """
        Class for formatting printer url.
        Stripes protocol from url
        """

        def format(self, value):
            parsed = urlparse.urlparse(value)
            return parsed.netloc + parsed.path

    @login_required
    @selective_marshal_with({
        "id": fields.Integer,
        "temperature": fields.Nested({
            "profiles": fields.List(
                fields.Nested({
                    "bed": fields.String,
                    "extruder": fields.String,
                    "name": fields.String
                })
            )
        }, attribute='settings.temperature')
    }, {
        "name": fields.String,
        "apikey": fields.String,
        "ip": ParsedUrl(attribute="url"),
    })
    def get(self):
        """
        Gets settings of printer.
        If user is superadmin, printer access data are included
        """
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        for printer in printers:
            try:
                ret = OctoprintService.get_settings(printer)
                ret["printerId"] = printer.id
                printer.settings = ret
            except (requests.ConnectionError, RuntimeError):
                pass
        return printers, 200

    @login_required
    def post(self):
        """Saves OctoPrint settings to printers"""
        args = printerIdParser.parse_args()
        printers = g.user.get_accessible_printers_id(args["printerId"])

        for printer in printers:
            try:
                OctoprintService.save_settings(printer, request.json)
            except (requests.ConnectionError, RuntimeError):
                pass

        socketio.emit("rejoin", broadcast=True, skip_sid=None)
        return "", 200
