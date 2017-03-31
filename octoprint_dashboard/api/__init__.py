from octoprint_dashboard import app
from flask_restful import Api
from .printer import PrinterApi
from .group import GroupApi
from .groupSettings import GroupSettingsApi
from .file import FileApi
from .printerStatus import PrinterStatusIdApi, PrinterStatusApi
from .user import UserApi
from .superadmin import SuperAdminApi

api = Api(app)

api.add_resource(PrinterApi, '/printer')
api.add_resource(GroupApi, '/group')
api.add_resource(GroupSettingsApi, '/group/settings/<int:group_id>')
api.add_resource(FileApi, '/printer/upload')
api.add_resource(PrinterStatusIdApi, '/printer/status/<int:printer_id>')
api.add_resource(PrinterStatusApi, '/printer/status')
api.add_resource(UserApi, '/user')
api.add_resource(SuperAdminApi, '/superadmin')
