/** @ngInject */
function ControlController(Files, Printer) {
  const $ctrl = this;

  this.uploadPrint = function (file) {
    Files.printFile(file, $ctrl.printers);
  };

  this.upload = function (file) {
    Files.uploadFile(file, $ctrl.printers);
  };

  this.setToolTemperature = function (temp) {
    Printer.setToolTemperature($ctrl.printers, temp);
  };

  this.setBedTemperature = function (temp) {
    Printer.setBedTemperature($ctrl.printers, temp);
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
