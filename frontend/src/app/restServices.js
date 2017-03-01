angular.module('restServices', [])
/** @ngInject */
.factory('Printer', $resource => {
  const printers = $resource('app/printers.json');
  const printerStatus = $resource('app/printerStatus.json', {printerId: '@id'});

  return {
    getPrinters: () => {
      return printers.get().$promise;
    },
    getPrinterStatus: printerId => {
      return printerStatus.get({printerId}).$promise;
    }
  };
})
/** @ngInject */
.factory('Files', $resource => {
  return {
    uploadFile: (file, printerId) => {
      const data = new FormData();
      data.append('file', file);

      return $resource('api/upload', {printerId: '@id'}, {
        update: {
          method: 'PUT',
          headers: {'Content-Type': undefined}
        }
      }).update({printerId}, data).$promise;
    },
    printFile: (file, printerId) => {
      const data = new FormData();
      data.append('file', file);

      return $resource('api/uploadPrint', {printerId: '@id'}, {
        update: {
          method: 'PUT',
          headers: {'Content-Type': undefined}
        }
      }).update({printerId}, data).$promise;
    }
  };
});
