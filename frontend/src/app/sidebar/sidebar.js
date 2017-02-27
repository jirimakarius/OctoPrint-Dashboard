/** @ngInject */
function SidebarController(Printer) {
  const $ctrl = this;

  Printer.getPrinters().then(response => {
    $ctrl.printers = response.data;
    // console.dir(response);
  });
}

export const sidebar = {
  template: require('./sidebar.html'),
  controller: SidebarController,
  bindings: {
    printers: '='
  }
};
