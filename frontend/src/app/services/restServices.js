angular.module('restServices', [])
/** @ngInject */
.factory('Printer', ($resource, ENV) => {
  const printers = $resource(`${ENV.api}/printer`);
  const printerIdStatus = $resource(`${ENV.api}/printer/status/:printerId`, {printerId: '@id'});
  const printerStatus = $resource(`${ENV.api}/printer/status`, {printerId: '@id'});

  return {
    getPrinters: () => {
      return printers.query().$promise;
    },
    addPrinter: printer => {
      return printers.save(printer).$promise;
    },
    removePrinters: printerArray => {
      return printers.remove({printerId: getCheckedPrinterId(printerArray)}).$promise;
    },
    getPrinterIdStatus: printerId => {
      return printerIdStatus.get({printerId}).$promise;
    },
    getPrinterStatus: () => {
      return printerStatus.query().$promise;
    },
    setToolTemperature: (printerArray, temperature) => {
      return printerStatus.save({printerId: getCheckedPrinterId(printerArray)}, {tool: temperature}).$promise;
    },
    setBedTemperature: (printerArray, temperature) => {
      console.dir(printerArray);
      console.dir(getCheckedPrinterId(printerArray));
      return printerStatus.save({printerId: getCheckedPrinterId(printerArray)}, {bed: temperature}).$promise;
    }
  };
})
/** @ngInject */
.factory('Files', ($resource, ENV) => {
  return {
    uploadFile: (file, printerArray) => {
      const data = new FormData();
      data.append('file', file);

      return $resource(`${ENV.api}/printer/upload`, {printerId: '@id'}, {
        upload: {
          method: 'POST',
          headers: {'Content-Type': undefined}
        }
      }).upload({printerId: getCheckedPrinterId(printerArray)}, data).$promise;
    },
    printFile: (file, printerArray) => {
      const data = new FormData();
      data.append('file', file);

      return $resource(`${ENV.api}/printer/upload`, {printerId: '@id', print: true}, {
        upload: {
          method: 'POST',
          headers: {'Content-Type': undefined}
        }
      }).upload({printerId: getCheckedPrinterId(printerArray)}, data).$promise;
    }
  };
})

/** @ngInject */
.factory('Group', ($resource, ENV) => {
  const groups = $resource(`${ENV.api}/group`);
  const groupSettings = $resource(`${ENV.api}/group/settings/:groupId`, {groupId: '@id'});

  return {
    getGroups: () => {
      return groups.query().$promise;
    },
    addGroup: group => {
      return groups.save(group).$promise;
    },
    getGroupSettings: groupId => {
      return groupSettings.get({groupId}).$promise;
    }
  };
})

/** @ngInject */
.factory('User', ($resource, ENV) => {
  const users = $resource(`${ENV.api}/user`);

  return {
    getUsers: () => {
      return users.query().$promise;
    }
  };
});

function getCheckedPrinterId(printers) {
  const id = [];
  printers.forEach(printer => {
    if (printer.checked) {
      id.push(printer.id);
    }
  });

  return id;
}
