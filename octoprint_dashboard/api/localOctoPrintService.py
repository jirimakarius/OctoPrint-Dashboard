from flask_restful import Resource, marshal_with, fields

from octoprint_dashboard.app import zeroconf_browser
from octoprint_dashboard.login import superadmin_required
from octoprint_dashboard.model import Printer


class LocalOctoPrintServiceApi(Resource):
    """
    Returns information about unsaved printers in local network.
    Uses zeroconf, multicast DNS service discovery
    """

    @superadmin_required
    @marshal_with({
        "ip": fields.String(attribute="server"),
        "name": fields.String
    })
    def get(self):
        result = list(zeroconf_browser.services.values())
        printers = Printer.query.all()
        for printer in printers:
            for service in result:
                if printer.url.split("//")[1] == service["ip"]:
                    result.remove(service)
        return result, 200
