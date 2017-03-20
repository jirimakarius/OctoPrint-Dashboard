from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse
from flask import request
import requests

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService

parser = reqparse.RequestParser()
parser.add_argument('printerId', type=int, required=True, help='Name can\'t be converted', action='append')
parser.add_argument('file', type=FileStorage, required=True, help='No file given', location='files')
parser.add_argument('print', type=bool, help='Print can\'t be converted')


class FileApi(Resource):
    @login_required
    def post(self):
        if not request.files["file"]:
            return "", 400
        args = parser.parse_args()
        # print(args)
        printers = Printer.query.filter(Printer.id.in_(args["printerId"])).all()
        for printer in printers:
            try:
                response = OctoprintService.send_file(printer, args["file"], args['print'])
            except RuntimeError:
                return None, 400
        return None, 200
