/** @ngInject */
function AdminController(Printer) {
  this.printers = [];

  Printer.getPrinters()
    .then(response => {
      this.printers = response.data;
    });
}

export const admin = {
  template: require('./admin.html'),
  controller: AdminController
};
