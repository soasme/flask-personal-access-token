// declare a new module called 'myApp', and make it require the `ng-admin` module as a dependency
var Admin = angular.module('Admin', ['ng-admin']);
// declare a function to run when the module bootstraps (during the 'config' phase)
Admin.config(['NgAdminConfigurationProvider', function (nga) {
  // create an admin application
  var applicationName = 'Personal Access Token Management Admininistration';
  var admin = nga.application(
    applicationName,
    window.g.debug
  ).baseApiUrl(window.g.baseApiUrl);
  // more configuration here later
  var token = nga.entity('tokens');
  admin.addEntity(token);

  token.listView().fields([
    nga.field('description'),
    nga.field('token'),
    nga.field('last_used_at'),
  ]).listActions([
    'delete',
    'show',
    'edit',
  ]);
  token.showView().fields([
    nga.field('description'),
    nga.field('token'),
    nga.field('last_used_at'),
  ]);
  token.creationView().fields([
    nga.field('description').validation({ required: true }),
  ]);
  token.editionView().fields([
    nga.field('description'),
  ]);

  // ...
  // attach the admin application to the DOM and execute it
  admin.menu(
    nga.menu()
      .addChild(nga.menu(token).icon('<span class="glyphicon glyphicon-pencil"></span>'))
  );

  nga.configure(admin);
}]);

Admin.config(['RestangularProvider', function(RestangularProvider) {
  RestangularProvider.addFullRequestInterceptor(
    function(element, operation, what, url, headers, params) {
      if (operation === "getList") {
        if (params._page) {
          params.offset = (params._page - 1) * params._perPage;
          params.limit = params._perPage;
        }
      }
      return {params: params};
    }
  );

  RestangularProvider.addResponseInterceptor(
    function(data, operation, what, url, response, deferred) {
      var extractedData;
      extractedData = data.data;
      return extractedData;
    }
  );

}]);
