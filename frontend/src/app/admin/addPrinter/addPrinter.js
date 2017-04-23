/** @ngInject */
function Controller($mdDialog, Printer) {
  const $ctrl = this;
  $ctrl.printers = [];

  this.$onInit = function () {
    Printer.getLocalServices()
      .then(result => {
        result.forEach(service => {
          $ctrl.printers.push({name: service.name, ip: service.ip, apikey: "", valid: "false"});
        });
      });
  };

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    Printer.addPrinter($ctrl.printers.filter(printer => {
      return printer.valid === "true";
    }))
      .then(() => {
        $mdDialog.hide();
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
