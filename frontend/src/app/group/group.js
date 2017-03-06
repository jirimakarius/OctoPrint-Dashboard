/** @ngInject */
function GroupController() {

}

export const group = {
  template: require('./group.html'),
  controller: GroupController,
  bindings: {
    group: '='
  }
};
