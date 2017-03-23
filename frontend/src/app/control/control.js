/** @ngInject */
function ControlController(Files, Printer) {
  const $ctrl = this;

  this.uploadPrint = function (file) {
    console.dir(file);
    if (file) {
      Files.printFile(file, $ctrl.printers);
      $ctrl.printers.forEach(printer => {
        if (printer.checked) {
          printer.state.state = "Preparing to print";
        }
      });
    }
  };

  this.upload = function (file) {
    if (file) {
      Files.uploadFile(file, $ctrl.printers);
    }
  };

  this.setToolTemperature = function (temp) {
    Printer.setToolTemperature($ctrl.printers, temp);
    $ctrl.printers.forEach(printer => {
      if (printer.checked) {
        printer.state.temperature.tool.target = temp;
      }
    });
    delete $ctrl.tool;
  };

  this.setBedTemperature = function (temp) {
    Printer.setBedTemperature($ctrl.printers, temp).then(response => {
      console.dir(response);
    });
    $ctrl.printers.forEach(printer => {
      if (printer.checked) {
        printer.state.temperature.bed.target = temp;
      }
    });
    delete $ctrl.bed;
  };

  this.checked = function () {
    return Printer.getCheckedPrinterId($ctrl.printers).length;
  };

  this.operational = function () {
    return Printer.operational($ctrl.printers);
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
