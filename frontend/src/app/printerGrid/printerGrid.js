/* @ngInject */
function PrinterGridController(Printer) {
  const $ctrl = this;

  Printer.getPrinters().then(response => {
    $ctrl.printers = response;
  });
}

export const printerGrid = {
  template: require('./printerGrid.html'),
  controller: PrinterGridController,
  bindings: {
    printers: '='
  },
  controllerAs: 'something'
};
