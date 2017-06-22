import socket

from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange


class ZeroconfBrowser:
    """
    Class for zeroconf multicast DNS service discovery of OctoPrint instances in local network
    """

    def __init__(self):
        self._zeroconf = None
        self._browser = None
        self.services = {}

    def start(self):
        """Start zeroconf browser"""
        self._zeroconf = Zeroconf()
        self._browser = ServiceBrowser(self._zeroconf, '_octoprint._tcp.local.',
                                       handlers=[self.on_service_state_change])

    def on_service_state_change(self, zeroconf, service_type, name, state_change):
        """
        Runs every time service in MDNS changes state(removed, added, modified).
        On service added, injects data to instance variable
        """
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                self.services["%s:%d" % (socket.inet_ntoa(info.address), info.port)] = {
                    "ip": "%s:%d" % (socket.inet_ntoa(info.address), info.port),
                    "server": info.server,
                    "service": name,
                    "name": name.split('"')[1] if len(name.split('"')) == 3 else None
                }
