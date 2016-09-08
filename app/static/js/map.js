var map = null
socket = null;

$(document).ready(function () {

    // Create the leaflet map
    map = createMap();

    // Create the web socket
    socket = io.connect('//' + document.domain + ':' + location.port);

    // Handle position update
    socket.on('positions_update', updatePositions);

});

/**
 * Create the leaflet map.
 * @returns {Array|*}
 */
function createMap() {

    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12, attribution: osmAttrib});

    map = new L.Map('map');
    map.setView(new L.LatLng(51.3, 0.7),9);
    map.addLayer(osm);

    return map;

}

function updatePositions(position) {

    console.log(position);

}