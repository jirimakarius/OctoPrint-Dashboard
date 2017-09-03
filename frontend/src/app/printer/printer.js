/** @ngInject */
function PrinterController(Printer) {
  const $ctrl = this;

  this.pause = function () {
    Printer.pausePrinter($ctrl.data.id).then(() => {
      if ($ctrl.data.state.text === "Printing") {
        // $ctrl.data.state.text = "Pausing...";
      }
      if ($ctrl.data.state.text === "Paused") {
        // $ctrl.data.state.text = "Resuming...";
      }
    });
  };
  this.cancel = function () {
    Printer.cancelPrinter($ctrl.data.id);
    // $ctrl.data.state.text = "Aborting job...";
  };

  this.progressHidden = function () {
    return !($ctrl.data.state.text === "Printing" || $ctrl.data.state.text === "Pausing..." || $ctrl.data.state.text === "Paused" || $ctrl.data.state.text === "Resuming...");
  };
}

export const printer = {
  template: require('./printer.html'),
  controller: PrinterController,
  bindings: {
    data: '='
  }
};
