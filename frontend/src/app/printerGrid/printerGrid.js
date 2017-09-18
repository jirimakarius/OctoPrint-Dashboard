/** @ngInject */
function PrinterGridController($auth, printersOfGroupFilter, socketIO, Group) {
  const $ctrl = this;
  // let interval = "";

  this.$onInit = function () {
    if ($auth.isAuthenticated()) {
      socketIO.on('reconnecting', () => {
        _.forEach($ctrl.printers, printer => {
          printer.state.text = "Connection lost";
        });
      });
      socketIO.on('reconnect', () => {
        socketIO.emit("join", {
          jwt: $auth.getToken()
        });
      });
      socketIO.on('rejoin', () => {
        socketIO.emit("join", {
          jwt: $auth.getToken()
        });
      });
      socketIO.emit("join", {
        jwt: $auth.getToken()
      });
      socketIO.on("printers", data => {
        _.forEach($ctrl.printers, printer => {
          printer.found = false;
        });
        _.forEach(data, printer => {
          let found = _.find($ctrl.printers, {id: printer.id});
          printer.found = true;
          if (found) {
            _.merge(found, printer);
          } else {
            $ctrl.printers.push(printer);
            found = _.last($ctrl.printers);
          }
          if (!found.state) {
            _.extend(found, {state: {text: "Offline/Unreachable"}, temps: [], job: {}, progress: {}});
          }
        });
        _.remove($ctrl.printers, value => {
          return !value.found;
        });
      });
      socketIO.on("status", data => {
        const printer = _.find($ctrl.printers, {id: data.id});
        if (printer) {
          _.merge(printer, data);
        } else {
          $ctrl.printers.push(data);
        }
      });
      Group.getGroups()
        .then(response => {
          $ctrl.groups = response;
        });
    }
  };

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
