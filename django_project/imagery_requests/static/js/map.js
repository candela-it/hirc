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
    var mapsize = map.getSize();
    var minim = mapsize.x * 0.03;
    var dist = getLayerSizePx(layer);
    var tmp_layers = layer.getLayers();

    // check layers in the layer group
    for (iLayer in tmp_layers) {
        // maker layer shuold not have an additional layer group as it's not subclassing L.FeatureGroup
        if (typeof tmp_layers[iLayer]._layers === 'undefined') {
            // set opacity of the marker
            if (dist > minim) {
                tmp_layers[iLayer].setOpacity(0);
            } else {
                tmp_layers[iLayer].setOpacity(1);
            }
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

    // initialize layerGroups
    var layergroupdefinition = ['Initiated', 'Processing', 'Done'];
    for (lg_id in layergroupdefinition) {
        var layergroup = layergroupdefinition[lg_id];
        layergroups[layergroup] = L.featureGroup();
        info.update('<p class="legend-item"><span class="box_' + layergroup +'"></span> '+layergroup+'</p>');
        map.addLayer(layergroups[layergroup]);
        control.addOverlay(layergroups[layergroup],layergroup);
    };

    //
    $.get("/worldjson", function(data) {
        _.each(data,  function(request) {
            var glayer_group = L.featureGroup();
            var glayer = L.geoJson(
                jQuery.parseJSON(request.polygon),
                {
                    style: {
                        'color': colors[request.status],
                        'weight': '1'
                    },
                    onEachFeature: function (feature, layer) {
                        var html = '<p class="popup_elem">'+request.title+'</p>'+'<p class="popup_elem">'+request.status+'</p>';

                        var center = layer.getBounds().getCenter();
                        var icon = L.MakiMarkers.icon({icon: "town", color: colors[request.status], size: "m"});

                        var l_marker = L.marker(center, {icon: icon})
                        // add marker layer to the layer group
                        l_marker.addTo(glayer_group);

                        // setup markerLayer events
                        $(l_marker).on('click', function() {
                             window.location = '/requests/' + request.id + '/';
                        });
                        $(l_marker).hover(
                            function() {
                                $('#popup').html(html).show();
                            },
                            function() {
                                $('#popup').hide();
                            }
                        );
                        // setup geojson layer events
                        $(layer).on('click', function() {
                            window.location = '/requests/' + request.id + '/';
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

            // add geojson layer to the layer group
            glayer.addTo(glayer_group);
            smartLayer(glayer_group);

            // add this layer group to the layergroup
            layergroups[request.status].addLayer(glayer_group);

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