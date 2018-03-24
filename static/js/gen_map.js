var bounds = new google.maps.LatLngBounds();
var map = new google.maps.Map(document.getElementById("map_canvas"), {
    zoom: 15,
});

var markers = points.map(point => {
    bounds.extend(new google.maps.LatLng(point.lat, point.lng));

    return new google.maps.Marker({
        position: point,
        map: map,
    });
});

map.fitBounds(bounds);
map.panToBounds(bounds);