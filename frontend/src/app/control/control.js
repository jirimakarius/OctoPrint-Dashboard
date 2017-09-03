/** @ngInject */
function ControlController(Files, Printer, $mdDialog, $document) {
  const $ctrl = this;

  this.uploadPrint = function (file) {
    if (file) {
      Files.uploadPrintFile(file, $ctrl.printers)
        .then(() => {
          $ctrl.getFiles();
        });
      $ctrl.printers.forEach(printer => {
        if (printer.checked) {
          printer.state.text = "Preparing to print";
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
    // $ctrl.printers.forEach(printer => {
    //   if (printer.checked) {
    //     printer.temps[0].tool0.target = temp;
    //   }
    // });
    delete $ctrl.tool;
  };

  this.setBedTemperature = function (temp) {
    Printer.setBedTemperature($ctrl.printers, temp);
    // $ctrl.printers.forEach(printer => {
    //   if (printer.checked) {
    //     printer.state.temperature.bed.target = temp;
    //   }
    // });
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

  this.getPresets = function () {
    Printer.getSettings($ctrl.printers)
      .then(response => {
        if (response.length) {
          $ctrl.temperaturePresets = response[0].temperature.profiles;
        }
      });
  };

  this.deleteFile = function (file) {
    Files.deleteFile(Printer.getCheckedPrinterId($ctrl.printers)[0], file)
      .then(() => {
        $ctrl.files.splice($ctrl.files.indexOf(file), 1);
      });
  };

  this.printing = function (file) {
    return file.name !== Printer.getCheckedPrinter($ctrl.printers)[0].job.file.name;
  };

  this.printFile = function (file) {
    Files.printFile(Printer.getCheckedPrinterId($ctrl.printers)[0], file);
    // Printer.getCheckedPrinter($ctrl.printers)[0].state.text = "Preparing to print";
  };

  this.getChecked = function (printers) {
    return Printer.getCheckedPrinter(printers);
  };

  this.sendFile = function ($event, file) {
    $mdDialog.show({
      template: `<md-dialog flex="50" style="max-height: 90%"><printer-select printers="$ctrl.printers" filename="${file.name}" layout="column"></printer-select></md-dialog>`,
      parent: angular.element($document.body),
      controller() {
        this.printers = $ctrl.printers;
        this.filename = $ctrl.filename;
      },
      controllerAs: '$ctrl',
      targetEvent: $event,
      clickOutsideToClose: true,
      fullscreen: true,
      autoWrap: false
    })
      .then(result => {
        Files.fileToPrinters(Printer.getCheckedPrinter($ctrl.printers)[0].id, result, file);
      })
      .catch(() => {});
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
