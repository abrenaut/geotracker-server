var map = null,
    markers = {},
    socket = null,
    route = null;

$(document).ready(function () {

    // Create the leaflet map
    map = createMap('map');

    // Create the web socket
    socket = io.connect('//' + document.domain + ':' + location.port, {'path': socketioPath});

    // Handle position update
    socket.on('positions_update', updatePositionsFromData);

    // Handle show route
    socket.on('show_route', showRoute);

});

/**
 * Create the leaflet map.
 * @returns {Array|*}
 */
function createMap(mapID) {

    var osmUrl = '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12, attribution: osmAttrib});

    map = new L.Map(mapID);
    map.setView([51.505, -0.09], 13);
    map.addLayer(osm);

    updatePositions(initialPositions);

    return map;

}

/**
 * Update the leaflet map with positions return by the server
 * @param data
 */
function updatePositionsFromData(data) {
    updatePositions(data.positions);
}

/**
 * Update the leaflet map with new positions
 * @param positions
 */
function updatePositions(positions) {
    var markerArray = [];
    var positionsLength = positions.length;
    for (var i = 0; i < positionsLength; i++) {
        markerArray.push(updatePosition(positions[i]))
    }

    // Update the zoom to fit all the markers
    if (markerArray.length > 0) {
        var markerGroup = L.featureGroup(markerArray);
        map.fitBounds(markerGroup.getBounds());
    }
}

/**
 * Update a position marker on the leaflet map
 * @param position
 */
function updatePosition(position) {
    // If the position is already on the map update it
    if (position.device_id in markers) {
        markers[position.device_id].setLatLng([position.latitude, position.longitude]);
    }
    // If not, create it
    else {
        var marker = L.marker([position.latitude, position.longitude]).addTo(map).on('click', getRoute);
        marker.device_id = position.device_id;
        markers[position.device_id] = marker;
    }

    return markers[position.device_id];
}

/**
 * Ask the server for a device previous locations
 * @param e
 */
function getRoute(e) {
    socket.emit('get_route', e.target.device_id);
}

/**
 * Show a device previous locations
 * @param data
 */
function showRoute(data) {

    if (route != null) {
        map.removeLayer(route);
    }

    var pathMarkers = [];
    var waypointLength = data.waypoints.length;
    for (var i = 0; i < waypointLength; i++) {
        pathMarkers.push(L.circle(data.waypoints[i], 2));
    }

    var path = new L.Polyline(data.waypoints, {
        weight: 3,
        opacity: 0.5,
        smoothFactor: 1
    });

    route = L.layerGroup(pathMarkers)
        .addLayer(path)
        .addTo(map);

}