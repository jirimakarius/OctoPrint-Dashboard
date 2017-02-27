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
});
