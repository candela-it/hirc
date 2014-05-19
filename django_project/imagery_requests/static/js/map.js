function initMap() {
    map = L.map('map').fitWorld().setZoom(2);
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osmTiles = L.tileLayer(osmUrl, {attribution: osmAttrib});
    // In the URL below, replace 'examples.map-zr0njcqy' with your map id.
    var mapboxUrl = 'https://{s}.tiles.mapbox.com/v3/examples.map-zr0njcqy/{z}/{x}/{y}.png';
    var mapboxAttrib = '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>';
    var mapboxTiles = L.tileLayer(mapboxUrl, {attribution: mapboxAttrib});

    var bingUrl = 'http://t{s}.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1398';
    var bingAttrib = '&copy; <a href="http://bing.com/maps">Bing Maps</a>';
    var bingTiles = new BingLayer(bingUrl, {subdomains: ['0', '1', '2', '3', '4'], attribution: bingAttrib});

    map.addLayer(bingTiles);
    $(document).ready(function(){
      var overlays = {
        'osm': osmTiles,
        'mapbox': mapboxTiles,
        'bing': bingTiles,
      };
    control = L.control.layers(overlays).addTo(map);
    });
}

function addWorldGeoJson() {
    var info = L.control({'position': 'bottomleft'});
    info.onAdd = function (map) {
        this.div = L.DomUtil.create('div', 'legend');
        $(this.div).html('<h2>LEGEND</h2');
        return this.div;
      };
    info.update = function (elem) {
        $(this.div).append(elem);
    };
    info.addTo(map);
    colors = {
        'Processing': 'red',
        'Done': 'green',
        'Initiated': 'blue'
    }
    layergroups = {};
    var bounds;
    $.get("/worldjson", function(data) {
        _.each(data,  function(requests, status) {
            layergroups[status] = L.featureGroup();
            layergroups[status].on('layeradd', function() {
                if (typeof bounds == 'undefined') bounds = layergroups[status].getBounds();
                bounds.extend(layergroups[status].getBounds())
                map.fitBounds(bounds);
            });
            _.each(requests, function(layer, id) {
                var glayer = L.geoJson(
                    jQuery.parseJSON(layer.polygon),
                    {
                        style: {
                            'color': colors[status],
                            'weight': '1'
                        },
                        onEachFeature: function (feature, layer) {
                            $(layer).on('click', function() {
                                window.location = '/requests/' + id + '/';
                            });
                        }
                    }
                );
                layergroups[status].addLayer(glayer);
                bounds.extend(layergroups[status].getBounds());
            });
            info.update('<p class="legend-item"><span class="box_' + status +'"></span> '+status+'</p>')
            map.addLayer(layergroups[status]);
            control.addOverlay(layergroups[status],status);
        });
        map.fitBounds(bounds);
    });
}