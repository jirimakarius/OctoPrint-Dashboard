export default angular.module('services.socketIO', ['btford.socket-io'])
/** @ngInject */
  .factory('socketIO', (socketFactory, $location) => {
    const ret = socketFactory({
      ioSocket: io.connect(`${$location.protocol()}://${$location.host()}:${$location.port()}`, {transports: ['websocket', 'polling']})
    });
    // ret.forward("printers");
    // ret.forward("status");
    return ret;
  });
