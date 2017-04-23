from octoprint_dashboard.app import app
from flask_restful import Api
from .printer import PrinterApi
from .group import GroupApi
from .groupSettings import GroupSettingsApi
from .file import FileApi, FileIdApi
from .printerStatus import PrinterStatusIdApi, PrinterStatusApi
from .printerSettings import PrinterSettingsApi
from .user import UserApi
from .superadmin import SuperAdminApi
from .config import ClientConfigApi, ConfigApi
from .localOctoPrintService import LocalOctoPrintServiceApi

api = Api(app)

api.add_resource(PrinterApi, '/printer')
api.add_resource(GroupApi, '/group')
api.add_resource(GroupSettingsApi, '/group/<int:group_id>/settings')
api.add_resource(FileApi, '/printer/upload')
api.add_resource(FileIdApi, '/printer/<int:printer_id>/files')
api.add_resource(PrinterStatusIdApi, '/printer/status/<int:printer_id>')
api.add_resource(PrinterStatusApi, '/printer/status')
api.add_resource(UserApi, '/user')
api.add_resource(SuperAdminApi, '/superadmin')
api.add_resource(ClientConfigApi, '/clientConfig')
api.add_resource(ConfigApi, '/config')
api.add_resource(PrinterSettingsApi, '/printer/settings')
api.add_resource(LocalOctoPrintServiceApi, '/printer/service/local')
