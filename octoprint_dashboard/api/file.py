from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request, g
import requests

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

uploadParser = reqparse.RequestParser()
uploadParser.add_argument('printerId', type=int, required=True, help='Id can\'t be converted', action='append')
uploadParser.add_argument('file', type=FileStorage, required=True, help='No file given', location='files')
uploadParser.add_argument('print', type=bool, help='Print can\'t be converted')

deleteParser = reqparse.RequestParser()
deleteParser.add_argument('origin', type=str, required=True, help='Origin can\'t be converted')
deleteParser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
deleteParser.add_argument('send', type=bool, help='Send can\'t be converted', location="json")

sendParser = reqparse.RequestParser()
sendParser.add_argument('printerId', type=list, required=True, help='PrinterID can\'t be converted', location="json")


class FileApi(Resource):
    @login_required
    def post(self):
        if not request.files["file"]:
            return "", 400
        args = uploadParser.parse_args()
        filename = args["file"].filename
        contents = args["file"].read()
        printers = g.user.get_accessible_printers_id(args["printerId"])
        for printer in printers:
            try:
                response = OctoprintService.send_file(printer, filename, contents, args['print'])
            except (RuntimeError, requests.ConnectionError):
                pass
        return "", 200


class FileIdApi(Resource):
    @login_required
    @marshal_with({
        "name": fields.String,
        "type": fields.String,
        "origin": fields.String
    })
    def get(self, printer_id):
        printer = g.user.get_printer_id(printer_id)
        if not printer:
            return "", 403
        try:
            files = OctoprintService.get_files(printer)
        except (RuntimeError, requests.ConnectionError):
            return [], 200
        return files["files"], 200

    @login_required
    def delete(self, printer_id):
        args = deleteParser.parse_args()
        printer = g.user.get_printer_id(printer_id)
        if not printer:
            return "", 403
        if OctoprintService.delete_file(printer, args["origin"], args["name"]):
            return "", 204

        return "", 409

    @login_required
    def post(self, printer_id):
        args = deleteParser.parse_args()
        printer = g.user.get_printer_id(printer_id)
        if not printer:
            return "", 403
        if args["send"]:
            printer_ids = sendParser.parse_args()
            printers = g.user.get_accessible_printers_id(printer_ids["printerId"])
            content = OctoprintService.get_file_contents(printer, args["origin"], args["name"])
            for dest_printer in printers:
                try:
                    OctoprintService.send_file(dest_printer, args["name"], content, False)
                except (RuntimeError, requests.ConnectionError):
                    pass
            return "", 200
        else:
            if OctoprintService.print(printer, args["origin"], args["name"]):
                return "", 200

            return "", 409
