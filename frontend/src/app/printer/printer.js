/* @ngInject */
function PrinterController(Printer, $interval) {
  const $ctrl = this;
  this.$onInit = function () {
    $interval(() => {
      if ($ctrl.data.checked) {
        Printer.getPrinterStatus($ctrl.data.id)
          .then(response => {
            angular.extend($ctrl.data, response);
          });
      }
    }, 5000);
  };
}

export const printer = {
  template: require('./printer.html'),
  controller: PrinterController,
  bindings: {
    data: '='
  }
};
