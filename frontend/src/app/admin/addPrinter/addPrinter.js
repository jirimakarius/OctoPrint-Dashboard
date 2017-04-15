/** @ngInject */
function Controller($mdDialog, Printer) {
  const $ctrl = this;
  $ctrl.printers = [];

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    Printer.addPrinter({name: $ctrl.name, apikey: $ctrl.apikey, ip: $ctrl.ip})
      .then(() => {
        $mdDialog.hide();
      })
      .catch(response => {
        $ctrl.addprinter.$setSubmitted();
        $ctrl.addprinter.$error.message = response.data.message;
      });
  };

  this.addPrinter = function (name, apikey, ip) {
    const printer = {name, apikey, ip};
    $ctrl.printers.push(printer);
    $ctrl.validatePrinter(printer);
    $ctrl.newprinter.name = "";
    $ctrl.newprinter.apikey = "";
    $ctrl.newprinter.ip = "";
  };

  this.validatePrinter = function (printer) {
    printer.valid = "progress";
    Printer.validate(printer)
      .then(() => {
        printer.valid = "true";
      })
      .catch(() => {
        printer.valid = "false";
      });
  };
}

export const addPrinter = {
  template: require('./addPrinter.html'),
  controller: Controller
};
