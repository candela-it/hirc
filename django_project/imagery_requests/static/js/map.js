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
      L.control.layers(overlays).addTo(map);
    });
}