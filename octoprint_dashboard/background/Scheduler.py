from apscheduler.schedulers.background import BackgroundScheduler

from octoprint_dashboard.model import Printer, Config
from octoprint_dashboard.services import OctoprintService


class Scheduler:
    """
    Class for managing and running background tasks
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        """
        Starts background tasks.
        """
        self.scheduler.start()
        printers = Printer.query.all()
        config = Config.query.first()
        for printer in printers:
            Printer.states[printer.id] = {}
            self.add_printer_status_job(printer, config.server_refresh)

    def add_printer_status_job(self, printer: Printer, seconds):
        """
        Add new status job
        Gets new status of printer every n seconds, where n is parameter seconds
        """
        self.scheduler.add_job(OctoprintService.inject_printer_state,
                               trigger='interval',
                               args=[printer],
                               id=str(printer.id),
                               seconds=seconds)

    def remove_printer_status_job(self, printer_ids):
        """
        Removes printer status task
        """
        for printer in printer_ids:
            self.scheduler.remove_job(str(printer))

    def reschedule(self, seconds):
        """
        Changes execution period of all running jobs to parameter seconds
        """
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            job.reschedule(trigger='interval', seconds=seconds)
