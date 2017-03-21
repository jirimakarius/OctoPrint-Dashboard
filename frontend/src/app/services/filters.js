angular.module('filterModule', [])
  .filter('secondsToDateTime', () => seconds => new Date(1970, 0, 1).setSeconds(seconds));
