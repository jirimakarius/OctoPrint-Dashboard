/** @ngInject */
function ControlController(Files) {
  const $ctrl = this;

  const getCheckedPrinterId = function () {
    const id = [];
    $ctrl.printers.forEach(printer => {
      if (printer.checked) {
        id.push(printer.id);
      }
    });

    return id;
  };

  this.uploadPrint = function (file) {
    Files.printFile(file, getCheckedPrinterId()).then(response => {
      console.dir(response);
    });
  };

  this.upload = function (file) {
    Files.uploadFile(file, getCheckedPrinterId());
  };
}

export const control = {
  template: require('./control.html'),
  controller: ControlController,
  bindings: {
    printers: '='
  }
};
