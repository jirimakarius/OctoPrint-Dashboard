from flask_restful import Resource
from flask import request

from octoprint_dashboard.login import login_required
from octoprint_dashboard.model import Printer
from octoprint_dashboard.services import OctoprintService


class FileApi(Resource):
    @login_required
    def post(self):
        # print(request.data)
        # print(request.args.getlist('printerId'))
        # print(request.files["file"].read())
        printer = Printer.query.get(17)
        if request.files["file"]:
            response = OctoprintService.send_file(printer, request.files["file"])
            print(response.text)
            return response.text, 201
        return "",200
