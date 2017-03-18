angular.module('restServices', [])
/** @ngInject */
.factory('Printer', ($resource, ENV) => {
  const printers = $resource(`${ENV.api}/printer`);
  const printerStatus = $resource(`${ENV.api}/printerStatus/:printerId`, {printerId: '@id'});

  return {
    getPrinters: () => {
      return printers.query().$promise;
    },
    addPrinter: printer => {
      return printers.save(printer).$promise;
    },
    removePrinters: printerArray => {
      return printers.save(getCheckedPrinterId(printerArray)).$promise;
    },
    getPrinterStatus: printerId => {
      return printerStatus.get({printerId}).$promise;
    }
  };
})
/** @ngInject */
.factory('Files', ($resource, ENV) => {
  return {
    uploadFile: (file, printerId) => {
      const data = new FormData();
      data.append('file', file);

      return $resource(`${ENV.api}/upload`, {printerId: '@id'}, {
        upload: {
          method: 'POST',
          headers: {'Content-Type': undefined}
        }
      }).upload({printerId}, data).$promise;
    },
    printFile: (file, printerId) => {
      const data = new FormData();
      data.append('file', file);

      return $resource(`${ENV.api}/upload`, {printerId: '@id', print: true}, {
        upload: {
          method: 'POST',
          headers: {'Content-Type': undefined}
        }
      }).upload({printerId}, data).$promise;
    }
  };
})

/** @ngInject */
.factory('Group', ($resource, ENV) => {
  const groups = $resource(`${ENV.api}/group`);
  const groupSettings = $resource(`${ENV.api}/groupSettings/:groupId`, {groupId: '@id'});

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
