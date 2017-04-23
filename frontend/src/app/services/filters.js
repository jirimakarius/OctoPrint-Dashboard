angular.module('filterModule', [])
  .filter('secondsToDateTime', () => seconds => new Date(1970, 0, 1).setSeconds(seconds))
  .filter('printersOfGroup', () => {
    return function (printers, group) {
      if (!group) {
        return printers;
      }
      return printers.filter(printer => {
        let result = false;
        printer.group.forEach(groupObject => {
          if (groupObject.name === group) {
            result = true;
          }
        });
        return result;
      });
    };
  });
