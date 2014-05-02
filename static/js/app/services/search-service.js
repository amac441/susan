years.factory('SearchService', function ($http, $q) {
    var api_url = "/5years/api/search/";
    var stay_url = "/5years/api/stay/";
    return {
        get_jobs: function (search) {
            var url = api_url + search + "/";
            var defer = $q.defer();
            $http({ method: 'GET', url: url }).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                })
                .error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },

        get_stay: function (stay_search, site) {
            var url = stay_url + stay_search + "/" + site;
            var defer = $q.defer();
            $http({ method: 'GET', url: url }).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                })
                .error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
    }
});