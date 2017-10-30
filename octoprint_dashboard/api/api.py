from flask import Blueprint
from flask_restful import Api

from . import PrinterApi, PrinterIdApi, GroupApi, GroupSettingsApi, FileApi, FileIdApi, PrinterStatusApi, UserApi, \
    SuperAdminApi, ClientConfigApi, PrinterSettingsApi, LocalOctoPrintServiceApi

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

"""Api definition"""
api.add_resource(PrinterApi, '/printer')
api.add_resource(PrinterIdApi, '/printer/<int:printer_id>')
api.add_resource(GroupApi, '/group')
api.add_resource(GroupSettingsApi, '/group/<int:group_id>/settings')
api.add_resource(FileApi, '/printer/upload')
api.add_resource(FileIdApi, '/printer/<int:printer_id>/files')
api.add_resource(PrinterStatusApi, '/printer/status')
api.add_resource(UserApi, '/user')
api.add_resource(SuperAdminApi, '/superadmin')
api.add_resource(ClientConfigApi, '/config/client')
api.add_resource(PrinterSettingsApi, '/printer/settings')
api.add_resource(LocalOctoPrintServiceApi, '/printer/service/local')
