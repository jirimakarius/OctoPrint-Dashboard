from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
import socket


class ZeroconfBrowser:
    def __init__(self):
        self._zeroconf = None
        self._browser = None
        self.services = {}

    def start(self):
        self._zeroconf = Zeroconf()
        self._browser = ServiceBrowser(self._zeroconf, '_octoprint._tcp.local.',
                                       handlers=[self.on_service_state_change])

    def on_service_state_change(self, zeroconf, service_type, name, state_change):
        # print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                self.services["%s:%d" % (socket.inet_ntoa(info.address), info.port)] = {
                    "ip": "%s:%d" % (socket.inet_ntoa(info.address), info.port),
                    "service": name,
                    "name": name.split('"')[1] if len(name.split('"')) == 3 else None
                }
