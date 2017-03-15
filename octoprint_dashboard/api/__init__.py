from octoprint_dashboard import app
from flask_restful import Api
from .printer import PrinterApi

api = Api(app)

api.add_resource(PrinterApi, '/printer')
