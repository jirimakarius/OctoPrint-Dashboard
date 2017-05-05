import requests
from flask import request, g
from flask_restful import Resource, reqparse, marshal_with, fields
from werkzeug.datastructures import FileStorage

from octoprint_dashboard.login import login_required
from octoprint_dashboard.services import OctoprintService

uploadParser = reqparse.RequestParser()  # parser for upload file post
uploadParser.add_argument('printerId', type=int, required=True, help='Id can\'t be converted', action='append')
uploadParser.add_argument('file', type=FileStorage, required=True, help='No file given', location='files')
uploadParser.add_argument('print', type=bool, help='Print can\'t be converted')

deleteParser = reqparse.RequestParser()  # parser for deleting files and sending from one printer to another
deleteParser.add_argument('origin', type=str, required=True, help='Origin can\'t be converted')
deleteParser.add_argument('name', type=str, required=True, help='Name can\'t be converted')
deleteParser.add_argument('send', type=bool, help='Send can\'t be converted', location="json")

sendParser = reqparse.RequestParser()  # parser for printer ids located in json of request
sendParser.add_argument('printerId', type=list, required=True, help='PrinterID can\'t be converted', location="json")


class FileApi(Resource):
    """
    Api class for file upload and print to multiple printers given by query argument
    """

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
                OctoprintService.send_file(printer, filename, contents, args['print'])
            except (RuntimeError, requests.ConnectionError):
                pass
        return "", 200


class FileIdApi(Resource):
    """
    Api class for operations with files on single printer
    """

    @login_required
    @marshal_with({
        "name": fields.String,
        "type": fields.String,
        "origin": fields.String
    })
    def get(self, printer_id):
        """Gets all files present on given printer"""
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
        """Deletes given file on printer"""
        args = deleteParser.parse_args()
        printer = g.user.get_printer_id(printer_id)
        if not printer:
            return "", 403
        if OctoprintService.delete_file(printer, args["origin"], args["name"]):
            return "", 204

        return "", 409

    @login_required
    def post(self, printer_id):
        """Send file from on printer to defined printers or prints given file"""
        args = deleteParser.parse_args()
        printer = g.user.get_printer_id(printer_id)
        if not printer:
            return "", 403
        if args["send"]:  # send file from one printer to defined printers
            printer_ids = sendParser.parse_args()
            printers = g.user.get_accessible_printers_id(printer_ids["printerId"])
            content = OctoprintService.get_file_contents(printer, args["origin"], args["name"])
            for dest_printer in printers:
                try:
                    OctoprintService.send_file(dest_printer, args["name"], content, False)
                except (RuntimeError, requests.ConnectionError):
                    pass
            return "", 200
        else:  # print file
            if OctoprintService.print(printer, args["origin"], args["name"]):
                return "", 200

            return "", 409
