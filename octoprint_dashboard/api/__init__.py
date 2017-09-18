from flask_restful import Api

from octoprint_dashboard.app import app
from .config import ClientConfigApi
from .file import FileApi, FileIdApi
from .group import GroupApi
from .groupSettings import GroupSettingsApi
from .localOctoPrintService import LocalOctoPrintServiceApi
from .printer import PrinterApi, PrinterIdApi
from .printerSettings import PrinterSettingsApi
from .printerStatus import PrinterStatusApi
from .superadmin import SuperAdminApi
from .user import UserApi

api = Api(app)

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
