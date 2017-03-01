function MainController() {
  this.printers = [];
}

export const main = {
  template: require('./index.html'),
  controller: MainController
};
