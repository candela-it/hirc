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

function initRequestFormMap() {
    // Initialise the FeatureGroup to store editable layers.
    var drawnItems = new L.FeatureGroup();

    drawnItems.on('layeradd', function() {
        map.fitBounds(drawnItems.getBounds());
    });

    // If area exists (i.e. we are editing previously saved request).
    if ( jQuery('#id_area_of_interest').val() != '') {
        var polygon = jQuery('#id_area_of_interest').val();
        // if polygon is in geojson
        if (polygon[0] == '{') {
            var geojsonFeature = jQuery.parseJSON(polygon);
            var parsed_polygon = L.geoJson(geojsonFeature)

            // Add multipolygon parts separately to use leaflet draw features.
            jQuery.each(parsed_polygon._layers, function(index_1, obj_1) {
                jQuery.each(obj_1._layers, function(index_2, obj_2) {
                    drawnItems.addLayer(obj_2);
                });
            });
        } else {
            // polygon is in wkt.
            var parsed_polygon = omnivore.wkt.parse(polygon);
            // Add multipolygon parts separately to use leaflet draw features.
            jQuery.each(parsed_polygon._layers, function(index_1, obj_1) {
                jQuery.each(obj_1._layers, function(index_2, obj_2) {
                    drawnItems.addLayer(obj_2);
                });
            });
        }
    }

    map.addLayer(drawnItems);

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
      draw: {
        polygon: {
          allowIntersection: false,
          drawError: {
                    color: '#e1e100',
                    message: 'Draw normal polygons!'
                },
                shapeOptions: {
                    color: '#FFA500'
                }
        },
            polyline: false,
            rectangle: false,
            circle: false,
            marker: false,
      },
        edit: {
            featureGroup: drawnItems
        }
    });

    map.addControl(drawControl);

    // Initial vars for custom error tooltip.
    errorShown = false;
    custom_tooltip = null;
    hideErrorTimeout = null;

    function show_custom_tooltip(error_string) {
        // Hide error tooltip if exists.
        hideErrorTooltip();

        custom_tooltip = new L.Tooltip(map);
        custom_tooltip.updateContent({text: error_string});
        custom_tooltip.showAsError();
        errorShown = true;
        // Hide the error after 2 seconds
        hideErrorTimeout = setTimeout(L.Util.bind(hideErrorTooltip), 2000);
    }

    function hideErrorTooltip() {
        errorShown = false;
        if (custom_tooltip) {
            clearHideErrorTimeout();
            custom_tooltip.dispose();
            custom_tooltip = null;
        }
    }

    function clearHideErrorTimeout() {
        if (hideErrorTimeout) {
            clearTimeout(hideErrorTimeout);
            hideErrorTimeout = null;
        }
    }

    // Signal if drawing is activated. Initially it's not active.
    var drawIsActive = false;
    // Signal if edition is saved. Used for draw:editstop event.
    var isEditionSaved = false;
    // Initial vars for multipolygon checks during drawing.
    var previous_point = null;
    var current_point = null;

    map.on('draw:drawstart', function (e) {
      drawIsActive = true;
    });

    map.on('draw:created', function (e) {
        var layer = e.layer;
        drawIsActive = false;

        drawnItems.addLayer(layer);

        var trouble_polygons = [];
        var layers = drawnItems.getLayers();  // Layers list.

        // Check after drawing: line segments intersection; point in another polygon;
        // polygon overlaps another polygon.
        // Important because sometimes checks during drawing are not made.
        // It can happen because sometimes map.on('click') event listener doesn't
        // "get" that click (e.g., when you draw points on map quickly).
        if (layers.length > 1) {

            var polygons = get_cleaned_polygons(layers);

            var result = check_after_drawing(polygons);
            var trouble_polygons = result.trouble_polygons;
            var error_messages = result.error_messages;

            // If there are trouble polygons make them red.
            if (trouble_polygons.length > 0) {
                var polygon_counter = 0;

                for (var key in drawnItems._layers) {
                    if($.inArray(polygon_counter, trouble_polygons) != -1) {
                        drawnItems._layers[key].setStyle({
                            fillColor: '#ca4c4d',
                            color: '#ca4c4d'
                        });
                    }
                    polygon_counter++;
                }
            }
        }

        // Dump geojson to textarea.
        var geojson_string = create_geojson_multipolygon_string();
        jQuery('#id_area_of_interest').val(geojson_string);

        if (trouble_polygons.length == 0) {
            // Empty multipolygon errors field.
            jQuery('#id_multipolygon_errors').val('');
        } else {
            // Put multipolygon errors text in textarea.
            error_string = '';

            jQuery.each(error_messages, function() {
                error_string += this + ' ';
            });

            jQuery('#id_multipolygon_errors').val(error_string);

            // Show error tooltip.
            show_custom_tooltip(error_string);
        }

        // Set previuos_point var to null because next polygon won't have
        // previous_point immediately.
        previous_point = null;
    });

    map.on('draw:drawstop', function (e) {
      drawIsActive = false;

      current_point = null;
      previous_point = null;
    });

    map.on('draw:edited', function (e) {
        // draw:edited gets called after saving edition, BUT before draw:editstop
        //(i.e. draw:editstop is called after both save and cancel edit).
        // So our custom logic that we want to implement after saving edition
        // should go in draw:editstop.

        isEditionSaved = true;
    });

    map.on('draw:editstop', function (e) {
        // If edition is saved do the checking process,
        // if not (i.e. canceled ) just pass.
        if (isEditionSaved == true) {
            var layers = drawnItems.getLayers();  // Layers list.
            var polygons = get_cleaned_polygons(layers);

            var result = check_after_drawing(polygons);
            var trouble_polygons = result.trouble_polygons;
            var error_messages = result.error_messages;

            // Set "error" color to trouble polygons and default color to
            // regular polygons.
            var polygon_counter = 0;

            for (var key in drawnItems._layers) {
                if($.inArray(polygon_counter, trouble_polygons) != -1) {
                    drawnItems._layers[key].setStyle({
                        fillColor: '#ca4c4d',
                        color: '#ca4c4d'
                    });
                } else {
                    // Set default color.
                    drawnItems._layers[key].setStyle({
                        fillColor: '#FFA500',
                        color: '#FFA500'
                    });
                }

                polygon_counter++;
            }

            // Dump geojson to textarea.
            var geojson_string = create_geojson_multipolygon_string();
            jQuery('#id_area_of_interest').val(geojson_string);

            if (trouble_polygons.length == 0) {
                // Empty multipolygon errors field.
                jQuery('#id_multipolygon_errors').val('');
            } else {
                // Put multipolygon errors text in textarea.
                error_string = '';

                jQuery.each(error_messages, function() {
                    error_string += this + ' ';
                });

                jQuery('#id_multipolygon_errors').val(error_string);

                // Show error tooltip.
                show_custom_tooltip(error_string);
            }
        }

        isEditionSaved = false;
    });

    map.on('draw:deleted', function (e) {
        var layers = drawnItems.getLayers();  // Layers list.
        var polygons = get_cleaned_polygons(layers);

        var result = check_after_drawing(polygons);
        var trouble_polygons = result.trouble_polygons;
        var error_messages = result.error_messages;

        // Set "error" color to trouble polygons and default color to
        // regular polygons.
        var polygon_counter = 0;

        for (var key in drawnItems._layers) {
            if($.inArray(polygon_counter, trouble_polygons) != -1) {
                drawnItems._layers[key].setStyle({
                    fillColor: '#ca4c4d',
                    color: '#ca4c4d'
                });
            } else {
                // Set default color.
                drawnItems._layers[key].setStyle({
                    fillColor: '#FFA500',
                    color: '#FFA500'
                });
            }

            polygon_counter++;
        }

        if (layers.length == 0) {
            // Empty area_of_interest text area.
            jQuery('#id_area_of_interest').val('');
            // Empty multipolygon errors field.
            jQuery('#id_multipolygon_errors').val('');
        } else {
            // Dump geojson to textarea.
            var geojson_string = create_geojson_multipolygon_string();
            jQuery('#id_area_of_interest').val(geojson_string);

            if (trouble_polygons.length == 0) {
                // Empty multipolygon errors field.
                jQuery('#id_multipolygon_errors').val('');
            } else {
                // Put multipolygon errors text in textarea.
                error_string = '';

                jQuery.each(error_messages, function() {
                    error_string += this + ' ';
                });

                jQuery('#id_multipolygon_errors').val(error_string);

                // Show error tooltip.
                show_custom_tooltip(error_string);
            }
        }
    });

    map.on('click', function(e) {
        // If drawing is activated check if new point is inside existing polygon or
        // new line segment intersects with any of the existing line segments.
        if (drawIsActive == true) {
            current_point = [e.layerPoint.x, e.layerPoint.y];
            var layers = drawnItems.getLayers();

            // If other polygons exist then go through the checking process.
            if (layers.length > 0) {
                polygons = get_cleaned_polygons(layers)

                // Check if current point is inside existing polygon,
                // (important only for the first point of polygon).
                // For each polygon check if current line segment intersects
                // any line segement of the polygon.
                jQuery.each(polygons, function() {
                    // If previous_point exists (means that line segment exists)
                    // check intersections.
                    if (previous_point) {
                        var p1 = {x: previous_point[0], y: previous_point[1]};
                        var p2 = {x: current_point[0], y: current_point[1]};

                        for (i=0, j=this.length-1;i<this.length; j=i++) {
                            var p3 = {x: this[i][0], y: this[i][1]};
                            var p4 = {x: this[j][0], y: this[j][1]};

                            var intersects = L.LineUtil.segmentsIntersect(p1, p2, p3, p4);

                            if (intersects == true) {
                                // Delete the last vertex.
                                drawControl._toolbars['draw']._modes.polygon.handler.deleteLastVertex();
                                // Revert value of current_point to previous_point.
                                current_point = previous_point;
                                // Show error tooltip.
                                show_custom_tooltip("Area shouldn't intersect with another area.")
                                return false; // break jquery each loop and current loop
                            }
                        }
                    } else {
                        var pointIsInPolygon = point_in_polygon(current_point, this);

                        // If current point is inside existing polygon then delete
                        // that point and show error message.
                        if (pointIsInPolygon == true) {
                            // Cancel drawing polygon.
                            drawControl._toolbars['draw']._modes.polygon.handler.disable();
                            // Show error tooltip.
                            show_custom_tooltip("Can't place point inside polygon.")
                            return false; // break jquery each loop
                        }
                    }
                });
            }
            // Set value of previous point to current_point for future.
            previous_point = current_point;
        }
    });

    map.on('mousemove', function(e) {
        if (errorShown) {
            custom_tooltip.updatePosition(e.latlng);
        }
    });


    function check_after_drawing(polygons) {
        var trouble_polygons = [];
        var error_messages = [];

        // Check if any polygon intersects any other polygon.
        // Check if any polygon covers any other polygon.
        // Check if polygon intersects itself. Leaflet Draw plugin does that
        // check during drawing, but not after polygons are edited.
        jQuery.each(polygons, function(index_a, poly_a) {

            jQuery.each(polygons, function(index_b, poly_b) {

                if (poly_b != poly_a) {

                    var result = polygon_intersects_polygon(
                                    error_messages, trouble_polygons,
                                    poly_a, index_a,
                                    poly_b, index_b);

                    trouble_polygons = result.trouble_polygons;
                    error_messages = result.error_messages;

                    var result = polygon_covers_polygon(
                                    error_messages, trouble_polygons,
                                    poly_a, index_a,
                                    poly_b, index_b);

                    trouble_polygons = result.trouble_polygons;
                    error_messages = result.error_messages;
                }
            });

            var result = polygon_intersects_itself(
                            error_messages, trouble_polygons,
                            poly_a, index_a);

            trouble_polygons = result.trouble_polygons;
            error_messages = result.error_messages;
        });

        return {
            trouble_polygons: trouble_polygons,
            error_messages: error_messages
        }
    }

    // Check if any line segment of any polygon intersects with any line
    // segment of any other polygon.
    function polygon_intersects_polygon(error_messages, trouble_polygons, poly_a, index_a, poly_b, index_b) {
        var error_message = "Area shouldn't intersect with another area.";

        for (var k = 0, h = poly_a.length - 1; k < poly_a.length; h = k++) {
            var p_1a = {x: poly_a[k][0], y: poly_a[k][1]};
            var p_2a = {x: poly_a[h][0], y: poly_a[h][1]};

            for (var e = 0, f = poly_b.length - 1; e < poly_b.length; f = e++) {
                var p_1b = {x: poly_b[e][0], y: poly_b[e][1]};
                var p_2b = {x: poly_b[f][0], y: poly_b[f][1]};

                var intersects = L.LineUtil.segmentsIntersect(p_1a, p_2a, p_1b, p_2b);

                if (intersects == true) {
                    if( $.inArray(index_a, trouble_polygons) == -1 ) {
                        trouble_polygons.push(index_a);
                    }

                    if ($.inArray(index_b, trouble_polygons) == -1 ) {
                        trouble_polygons.push(index_b);
                    }

                    if ($.inArray(error_message, error_messages) == -1 ) {
                        error_messages.push(error_message);
                    }
                }
            }
        }

        return {
            trouble_polygons: trouble_polygons,
            error_messages: error_messages
        }
    }

    // Check if any polygon covers any other polygon. We're actually checking
    // if point from one polygon lies inside another polygon.
    function polygon_covers_polygon(error_messages, trouble_polygons, poly_a, index_a, poly_b, index_b) {
        var error_message = "Area shouldn't cover another area.";

        jQuery.each(poly_a, function(point_index, point) {
            var pointIsInPolygon = point_in_polygon(point, poly_b);

            if (pointIsInPolygon == true) {
                if( $.inArray(index_a, trouble_polygons) == -1 ) {
                    trouble_polygons.push(index_a);
                }

                if( $.inArray(index_b, trouble_polygons) == -1 ) {
                    trouble_polygons.push(index_b);
                }

                if ($.inArray(error_message, error_messages) == -1 ) {
                    error_messages.push(error_message);
                }
            }
        });

        return {
            trouble_polygons: trouble_polygons,
            error_messages: error_messages
        }
    }

    function polygon_intersects_itself(error_messages, trouble_polygons, poly_a, index_a) {
        var error_message = "Area shouldn't intersect with itself.";

        for (var i = 0, j = poly_a.length - 1; i < poly_a.length; j = i++) {
            var p_1 = {x: poly_a[i][0], y: poly_a[i][1]}
            var p_2 = {x: poly_a[j][0], y: poly_a[j][1]}

            for (var k = 0, h = poly_a.length - 1; k < poly_a.length; h = k++) {
                var p_3 = {x: poly_a[h][0], y: poly_a[h][1]}
                var p_4 = {x: poly_a[k][0], y: poly_a[k][1]}

                if (p_3 != p_1 && p_4 != p_2) {
                    var intersects = L.LineUtil.segmentsIntersect(p_1, p_2, p_3, p_4);

                    if (intersects == true) {
                        if( $.inArray(index_a, trouble_polygons) == -1 ) {
                            trouble_polygons.push(index_a);
                        }

                        if ($.inArray(error_message, error_messages) == -1 ) {
                            error_messages.push(error_message);
                        }
                    }
                }
            }
        }

        return {
            trouble_polygons: trouble_polygons,
            error_messages: error_messages
        }
    }

    // Function that checks if point is inside polygon.
    function point_in_polygon (point, polygon) {
        var x = point[0], y = point[1];

        var inside = false;
        for (var i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
            var xi = polygon[i][0], yi = polygon[i][1];
            var xj = polygon[j][0], yj = polygon[j][1];

            var intersect = ((yi > y) != (yj > y))
                && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
            if (intersect) inside = !inside;
        }
        return inside;
    }

    function get_cleaned_polygons(layers) {
        var polygons = [];

        // For each layer (polygon) get it's points coords. in pixels.
        jQuery.each(layers, function () {
            var polygon_points = this._originalPoints;
            var clean_polygon_points = [];

            jQuery.each(polygon_points, function() {
                clean_polygon_points.push([this.x, this.y]);
            });

            polygons.push(clean_polygon_points);
        });

        return polygons;
    }

    function create_geojson_multipolygon_string() {
        var geojson_string = '{"type": "MultiPolygon","coordinates": [';

        for (var key in drawnItems._layers) {
            var layer = drawnItems._layers[key];
            geojson_string += JSON.stringify(layer.toGeoJSON()['geometry']['coordinates']) + ',';
        }

        geojson_string = geojson_string.slice(0, -1);  // remove last comma.
        geojson_string += ']}';  // finish geojson string.

        return geojson_string
    }

    function create_geojson_polygon_string() {
        var geojson_string = '{"type": "Polygon","coordinates": [';
    }
}