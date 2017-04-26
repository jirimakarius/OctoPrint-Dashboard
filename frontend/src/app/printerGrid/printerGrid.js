/** @ngInject */
function PrinterGridController(Printer, $interval, $filter, $auth, $rootScope, Group, printersOfGroupFilter) {
  const $ctrl = this;
  let interval = "";

  this.$onInit = function () {
    if ($auth.isAuthenticated()) {
      Printer.getPrinterStatus()
        .then(response => {
          $ctrl.printers = response;
        });
      Group.getGroups()
        .then(response => {
          $ctrl.groups = response;
        });

      $rootScope.configPromise.then(() => {
        interval = $interval(() => {
          Printer.getPrinterStatus()
            .then(mergePrinterStatus);
        }, $rootScope.config.refresh * 1000);
      });
    }
  };

  this.$onDestroy = function () {
    $interval.cancel(interval);
  };

  function mergePrinterStatus(response) {
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
  }

  this.select = function (group) {
    $ctrl.printers.forEach(printer => {
      printer.checked = false;
    });

    if ($ctrl.selectedGroup === group) {
      printersOfGroupFilter($ctrl.printers, group)
        .forEach(printer => {
          printer.checked = true;
        });
    }

    $ctrl.selectedGroup = group;
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
