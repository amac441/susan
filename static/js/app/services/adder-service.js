years.factory('AdderService', function ($http, $q) {

    var api_url = "/5years/api/adder/";

    return {
        //get: function (post_id) {
        //    var url = api_url + post_id + "/";
        //    var defer = $q.defer();
        //    $http({method: 'GET', url: url}).
        //        success(function (data, status, headers, config) {
        //            defer.resolve(data);
        //        })
        //        .error(function (data, status, headers, config) {
        //            defer.reject(status);
        //        });
        //    return defer.promise;
        //},
        list: function () {
            var defer = $q.defer();
            $http({method: 'GET', url: api_url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },

        update: function (adder) {
            if (adder.id == '') {
                var url = api_url;
                var defer = $q.defer();
                $http({
                    method: 'PUT',
                    url: url,
                    data: adder
                }).
                    success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                return defer.promise;
            }
            else
            {
                var url = api_url + adder.id + "/";
                var defer = $q.defer();
                adder.id = '';
                $http({
                    method: 'DELETE',
                    url: url,
                    data: adder
                }).
                    success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                return defer.promise;


            }

            // call this from the toggle active deal in the feed controller
        },

    };
});