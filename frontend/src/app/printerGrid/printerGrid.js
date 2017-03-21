/** @ngInject */
function PrinterGridController(Printer, $interval, $filter, $auth) {
  const $ctrl = this;

  this.$onInit = function () {
    if ($auth.isAuthenticated()) {
      Printer.getPrinterStatus()
        .then(response => {
          $ctrl.printers = response;
        });

      $interval(() => {
        Printer.getPrinterStatus()
          .then(response => {
            const foundPrinters = new Array($ctrl.printers.length);

            response.forEach(printer => {
              const oldPrinter = $filter('filter')($ctrl.printers, data => {
                return printer.id === data.id;
              });
              if (oldPrinter.length) {
                foundPrinters[$ctrl.printers.indexOf(oldPrinter)] = 1;
                angular.extend(oldPrinter[0], printer);
              } else {
                $ctrl.printers.push(printer);
              }
            });

            foundPrinters.forEach((printer, index) => {
              if (!printer) {
                $ctrl.printers.splice(index, 1);
              }
            });
            // angular.merge($ctrl.printers, response);
          });
      }, 5000);
    }
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
