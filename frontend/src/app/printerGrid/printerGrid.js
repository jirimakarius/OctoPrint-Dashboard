/* @ngInject */
function PrinterGridController(Printer, $interval, $filter) {
  const $ctrl = this;

  Printer.getPrinterStatus()
    .then(response => {
      $ctrl.printers = response;
    });

  this.$onInit = function () {
    $interval(() => {
      Printer.getPrinterStatus()
        .then(response => {
          response.forEach(printer => {
            const oldPrinter = $filter('filter')($ctrl.printers, data => {
              return printer.id === data.id;
            });
            console.dir(oldPrinter);
            printer.checked = oldPrinter[0].checked;
          });

          $ctrl.printers = response;
        });
    }, 5000);
  };
}

export const printerGrid = {
  template: require('./printerGrid.html'),
  controller: PrinterGridController,
  bindings: {
    printers: '='
  },
  controllerAs: 'something'
};
