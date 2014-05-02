years.controller('AdderController', function ($scope, $routeParams, $location, AdderService, GlobalService, events) {
    $scope.events = events;
    $scope.globals = GlobalService;
    var failureCb = function (status) {
        console.log(status);
    }
    //options for modals
    $scope.opts = {
        backdropFade: true,
        dialogFade: true
    };

    // --------- ADD ITEM -----------

    $scope.addItem = function () {
        SearchService.add_item($scope.sender, $scope.recipient, $scope.subject, $scope.details).then(function (data) {
            $scope.items = data;
        }
        )
    };

    //$scope.events = [
    //  {
    //      desc: "testing this out",
    //      date: "May 12, 2014",
    //      id: 1, text: "Task A-12458",
    //      start_date: new Date(2014, 04, 08, 9, 0),
    //      end_date: new Date(2014, 04, 09, 16, 0),
    //  },
    //  {
    //      id: 2, text: "Task A-83473",
    //      start_date: new Date(2014, 04, 22, 9, 0),
    //      end_date: new Date(2014, 04, 24, 16, 0),
    //      desc: "testing this out",
    //      date: "May 12, 2014"
    //  }
    //];


    $scope.scheduler = { date: new Date(2014, 3, 1) };

});
