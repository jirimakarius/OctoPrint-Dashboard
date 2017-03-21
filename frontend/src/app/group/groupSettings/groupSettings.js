/** @ngInject */
function GroupSettingsController($mdDialog, Group, User) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.addUser = function () {
    const resource = $ctrl.searchTextUser.split(" ");
    resource.forEach(username => {
      if (findByUsername(username).length) {
      } else {
        $ctrl.groupsettings.users.push({
          username,
          role: 'user'
        });
      }
    });
    $ctrl.searchTextUser = null;
  };

  this.removeUser = function (index) {
    $ctrl.groupsettings.users.splice(index, 1);
  };

  this.$onInit = () => {
    Group.getGroupSettings($ctrl.group.id)
      .then(response => {
        $ctrl.groupsettings = response;
      });
    User.getUsers()
      .then(response => {
        $ctrl.users = response;
      });
  };

  this.querySearch = query => {
    return query ? $ctrl.printers.filter(createFilterForPrinter(query)) : [];
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
  function createFilterForPrinter(query) {
    const lowercaseQuery = angular.lowercase(query);

    return function filterFn(item) {
      return (angular.lowercase(item.name).indexOf(lowercaseQuery) === 0);
    };
  }
  function createFilterForUser(query) {
    const lowercaseQuery = angular.lowercase(query);

    return function filterFn(item) {
      return (angular.lowercase(item.username).indexOf(lowercaseQuery) === 0);
    };
  }

  function findByUsername(username) {
    return $ctrl.groupsettings.users.filter(user => {
      return user.username === username;
    });
  }

  this.userSearch = function (query) {
    return query ? $ctrl.users.filter(createFilterForUser(query)) : $ctrl.users;
  };
}

export const groupSettings = {
  template: require('./groupSettings.html'),
  controller: GroupSettingsController,
  bindings: {
    group: '=',
    printers: '='
  }
};
