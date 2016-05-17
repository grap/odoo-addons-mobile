'use strict';


angular.module('scan_to_purchase').factory(
        'ProductProductModel', [
        '$q', '$rootScope', 'jsonRpc',
        function ($q, $rootScope, jsonRpc) {

    return {
        LoadProduct: function() {
            return jsonRpc.searchRead(
                    'product.product', [], [
                    'id', 'name', 'default_code', 'ean13', 'uom_id',
                    'qty_available', 'virtual_available',
                    ]).then(function (res) {
                $rootScope.ProductListByEan13 = {}
                angular.forEach(res.records, function(product) {
                    if (product['ean13']){
                        $rootScope.ProductListByEan13[product['ean13']] = product;
                    }
                });
                return res.records.length;
            });
        },

    };
}]);
