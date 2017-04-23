/** @ngInject */
function PrinterController(Printer) {
  const $ctrl = this;

  this.pause = function () {
    Printer.pausePrinter($ctrl.data.id).then(() => {
      if ($ctrl.data.state.state === "Printing") {
        $ctrl.data.state.state = "Pausing...";
      }
      if ($ctrl.data.state.state === "Paused") {
        $ctrl.data.state.state = "Resuming...";
      }
    });
  };
  this.cancel = function () {
    Printer.cancelPrinter($ctrl.data.id);
    $ctrl.data.state.state = "Aborting job...";
  };

  this.progressHidden = function () {
    return !($ctrl.data.state.state === "Printing" || $ctrl.data.state.state === "Pausing..." || $ctrl.data.state.state === "Paused" || $ctrl.data.state.state === "Resuming...");
  };
}

export const printer = {
  template: require('./printer.html'),
  controller: PrinterController,
  bindings: {
    data: '='
  }
};
