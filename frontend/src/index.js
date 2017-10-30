import angular from 'angular';

import {main} from './app/main/index';
import {toolbar} from './app/toolbar/toolbar';
import {printer} from './app/printer/printer';
import {control} from './app/control/control';
import {printerGrid} from './app/printerGrid/printerGrid';
import {admin} from './app/admin/admin';
import {group} from './app/group/group';
import {addPrinter} from './app/admin/addPrinter/addPrinter';
import {addGroup} from './app/admin/addGroup/addGroup';
import {addSuperAdmin} from './app/admin/addSuperAdmin/addSuperAdmin';
import {groupSettings} from './app/group/groupSettings/groupSettings';
import {printerSettings} from './app/admin/printerSettings/printerSettings';
import {printerSelect} from './app/control/printerSelect/printerSelect';

import './app/services/restServices';
import './config';
import './app/services/filters';
import 'angular-ui-router';
import 'angular-animate';
import 'angular-aria';
import 'angular-messages';
import 'angular-material';
import 'angular-material/angular-material.css';
import 'angular-resource';
import 'angular-sortable-view';
import 'satellizer';
import 'ng-file-upload';
import 'angular-socket-io';
import 'lodash';

import routesConfig from './routes';
import eventListeners from './app/services/eventListeners';
import './app/services/socketio';
import './app/services/auth';

import './index.css';

export const app = 'app';
/** @ngInject */
angular
    .module(app, ['ui.router', 'ngMessages', 'ngMaterial', 'satellizer', 'ngResource', 'restServices', 'angular-sortable-view', 'ngFileUpload', 'app.config', 'filterModule', 'btford.socket-io', 'services.socketIO', 'authServices'])
    .config(routesConfig)
    .component('main', main)
    .component('toolbar', toolbar)
    .component('printer', printer)
    .component('control', control)
    .component('printerGrid', printerGrid)
    .component('admin', admin)
    .component('group', group)
    .component('addPrinter', addPrinter)
    .component('addGroup', addGroup)
    .component('addSuperAdmin', addSuperAdmin)
    .component('groupSettings', groupSettings)
    .component('printerSettings', printerSettings)
    .component('printerSelect', printerSelect)
    .run(eventListeners);
