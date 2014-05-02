years.controller('SearchController', function ($scope, $routeParams, SearchService, GlobalService, search) {
    $scope.search = search;

    $scope.globals = GlobalService;

    var failureCb = function (status) {
        console.log(status);
    }

    //calling search service
    $scope.searchFor = function () {
        SearchService.get($scope.search).then(function (data) {
            $scope.search = data;
            }
        )
    };
});