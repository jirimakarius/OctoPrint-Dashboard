/** @ngInject */
function ControlController(Files, Printer) {
  const $ctrl = this;

  this.uploadPrint = function (file) {
    console.dir(file);
    if (file) {
      Files.uploadPrintFile(file, $ctrl.printers)
        .then(() => {
          $ctrl.getFiles();
        });
      $ctrl.printers.forEach(printer => {
        if (printer.checked) {
          printer.state.state = "Preparing to print";
        }
      });
    }
  };

  this.upload = function (file) {
    if (file) {
      Files.uploadFile(file, $ctrl.printers)
        .then(() => {
          $ctrl.getFiles();
        });
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

  this.getFiles = function () {
    Files.getFiles(Printer.getCheckedPrinterId($ctrl.printers)[0])
      .then(response => {
        $ctrl.files = response;
      });
  };

  this.deleteFile = function (file) {
    Files.deleteFile(Printer.getCheckedPrinterId($ctrl.printers)[0], file)
      .then(() => {
        $ctrl.files.splice($ctrl.files.indexOf(file), 1);
      });
  };

  this.deleteAction = function (file) {
    return file.name !== Printer.getCheckedPrinter($ctrl.printers)[0].state.job.fileName;
  };

  this.printFile = function (file) {
    Files.printFile(Printer.getCheckedPrinterId($ctrl.printers)[0], file);
    Printer.getCheckedPrinter($ctrl.printers)[0].state.state = "Preparing to print";
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
