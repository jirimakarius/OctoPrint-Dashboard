/** @ngInject */
function PrinterController() {
  // const $ctrl = this;

}

export const printer = {
  template: require('./printer.html'),
  controller: PrinterController,
  bindings: {
    data: '='
  }
};
