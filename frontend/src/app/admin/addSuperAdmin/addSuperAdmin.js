/** @ngInject */
function Controller($mdDialog, User) {
  const $ctrl = this;

  this.cancel = function () {
    $mdDialog.cancel();
  };

  this.submit = function () {
    User.superAdminize($ctrl.searchTextUser).then(() => {
      $mdDialog.hide();
    });
  };

  this.$onInit = () => {
    User.getUsers()
            .then(response => {
              $ctrl.users = response;
            });
  };

  function createFilterForUser(query) {
    const lowercaseQuery = angular.lowercase(query);

    return function filterFn(item) {
      return (angular.lowercase(item.username).indexOf(lowercaseQuery) === 0);
    };
  }

  this.userSearch = function (query) {
    return query ? $ctrl.users.filter(createFilterForUser(query)) : $ctrl.users;
  };
}

export const addSuperAdmin = {
  template: require('./addSuperAdmin.html'),
  controller: Controller
};
