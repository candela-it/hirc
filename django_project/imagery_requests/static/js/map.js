function initMap() {
    map = L.map('map').setView([0,0],2);
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

    var bingUrlDate = 'http://mvexel.dev.openstreetmap.org/bingimageanalyzer/tile.php?t={q}';
    var bingTilesDate = new BingLayer(bingUrlDate, {subdomains: ['0', '1', '2', '3', '4'], attribution: bingAttrib});

    map.addLayer(bingTiles);
    $(document).ready(function(){
      var overlays = {
        'osm': osmTiles,
        'mapbox': mapboxTiles,
        'bing': bingTiles
      };
    control = L.control.layers(overlays).addTo(map);
    control.addOverlay(bingTilesDate, 'Bing tile age');
    });
}

function getLayerSizePx(layer) {
    var bounds = layer.getBounds();
    var sw = map.project(bounds.getSouthWest());
    var ne = map.project(bounds.getNorthEast());
    var dist = Math.sqrt( Math.pow((sw.x - ne.x),2) + Math.pow((sw.y - ne.y),2));
    return dist;
}

function smartLayer(layer) {
    if (typeof layer._layers != 'undefined') {
        var mapsize = map.getSize();
        var minim = mapsize.x*0.03;
        var dist = getLayerSizePx(layer);
        if (dist > minim) {
            layerMarkers[layer._leaflet_id].setOpacity(0);
        } else {
            layerMarkers[layer._leaflet_id].setOpacity(1);
        }
    }
}

function addWorldGeoJson() {
    // legend HTML and functions
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

    // color definitions for legend
    colors = {
        'Processing': '#FF0000',
        'Done': '#00FF00',
        'Initiated': '#0000FF'
    }

    layergroups = {};
    var bounds;
    layerMarkers = {};
    layerPopups = {};

    // mouse position tracking for hover popup
    var mouseX;
    var mouseY;
    $(document).mousemove( function(e) {
       mouseX = e.pageX - 100;
       mouseY = e.pageY - 55;
       $('#popup').css({'top':mouseY+'px', 'left': mouseX + 'px'});
    });

    //
    $.get("/worldjson", function(data) {
        _.each(data,  function(requests, status) {
            layergroups[status] = L.featureGroup();
            layergroups[status].on('layeradd', function(ev) {
                if (typeof ev.layer._layers != 'undefined') {
                    var html = _.find(ev.layer._layers, function (x) { return x.popup })
                    var center = ev.layer.getBounds().getCenter();
                    var icon = L.MakiMarkers.icon({icon: "town", color: colors[status], size: "m"});
                    layerMarkers[ev.layer._leaflet_id] = L.marker(center, {icon: icon})
                    layerMarkers[ev.layer._leaflet_id].addTo(this);
                    $(layerMarkers[ev.layer._leaflet_id]).on('click', function() {
                        window.location = '/requests/' + html.popupid + '/';
                    });
                    $(layerMarkers[ev.layer._leaflet_id]).hover(
                        function() {
                            $('#popup').html(html.popup).show();
                        },
                        function() {
                            $('#popup').hide();
                        }
                    );
                }
                smartLayer(ev.layer);
            });
            _.each(requests, function(layer, id) {
                var title = layer.title;
                var glayer = L.geoJson(
                    jQuery.parseJSON(layer.polygon),
                    {
                        style: {
                            'color': colors[status],
                            'weight': '1'
                        },
                        onEachFeature: function (feature, layer) {
                            var html = '<p class="popup_elem">'+title+'</p>'+'<p class="popup_elem">'+status+'</p>';
                            layer.popup = html;
                            layer.popupid = id;
                            layerPopups[layer._leaflet_id] = html;
                            layer.popup = html;
                            $(layer).on('click', function() {
                                window.location = '/requests/' + id + '/';
                            });
                            $(layer).hover(
                                function() {
                                    $('#popup').html(html).show();
                                },
                                function() {
                                    $('#popup').hide();
                                }
                            );
                        }
                    }
                );
                layergroups[status].addLayer(glayer);
            });
            info.update('<p class="legend-item"><span class="box_' + status +'"></span> '+status+'</p>')
            map.addLayer(layergroups[status]);
            control.addOverlay(layergroups[status],status);
        });
        map.on('zoomend', function() {
            _.each(layergroups, function(layerg, status) {
                layerg.eachLayer(function (layer) {
                    smartLayer(layer);
                });
            });
        });
    });
}