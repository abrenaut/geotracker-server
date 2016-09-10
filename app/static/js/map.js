var map = null,
    markers = [];

$(document).ready(function () {

    // Create the leaflet map
    map = createMap('map');

    // Create the web socket
    var socket = io.connect('//' + document.domain + ':' + location.port);

    // Handle position update
    socket.on('positions_update', updatePositions);

});

/**
 * Create the leaflet map.
 * @returns {Array|*}
 */
function createMap(mapID) {

    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12, attribution: osmAttrib});

    map = new L.Map(mapID);
    map.setView(new L.LatLng(47.6, -2.7), 9);
    map.addLayer(osm);

    var initialPositions = $('#' + mapID).data('initial-positions');

    $.each(initialPositions, function (i, position) {
        updatePosition(position);
    });

    return map;

}

function updatePositions(data) {
    var positions = data.positions;
    var positionsLength = data.positions.length;
    for (var i = 0; i < positionsLength; i++) {
        updatePosition(positions[i])
    }
}


function updatePosition(position) {
    if (position.device_id in markers) {
        markers[position.device_id].setLatLng([position.latitude, position.longitude]);
    } else {
        markers[position.device_id] = L.marker([position.latitude, position.longitude]).addTo(map);
    }
}