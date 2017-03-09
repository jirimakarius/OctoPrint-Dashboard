/** @ngInject */
function GroupSettingsController($mdDialog, Group) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.addUser = function () {
    if (findByUsername($ctrl.username).length) {
    } else {
      $ctrl.group.users.push({
        username: $ctrl.username,
        role: 'user'
      });
    }
    $ctrl.username = null;
  };

  this.removeUser = function (index) {
    $ctrl.group.users.splice(index, 1);
  };

  this.$onInit = () => {
    Group.getGroupSettings($ctrl.group.id)
      .then(response => {
        $ctrl.group = response;
      });
  };

  this.selectedItem = null;
  this.searchText = null;
  this.querySearch = query => {
    return query ? $ctrl.printers.filter(createFilterFor(query)) : [];
  };
  this.transformChip = chip => {
    if (angular.isObject(chip)) {
      return chip;
    }
    // Otherwise, create a new one
    return {name: chip, type: 'new'};
  };
  /**
   * Create filter function for a query string
   */
  function createFilterFor(query) {
    const lowercaseQuery = angular.lowercase(query);

    return function filterFn(printer) {
      return (angular.lowercase(printer.name).indexOf(lowercaseQuery) === 0);
    };
  }

  function findByUsername(username) {
    return $ctrl.group.users.filter(user => {
      return user.username === username;
    });
  }
}

export const groupSettings = {
  template: require('./groupSettings.html'),
  controller: GroupSettingsController,
  bindings: {
    group: '=',
    printers: '='
  }
};
