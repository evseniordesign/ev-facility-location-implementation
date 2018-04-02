var bounds = new google.maps.LatLngBounds();
var map = new google.maps.Map(document.getElementById("map_canvas"), {
    zoom: 15,
});

unassigned.forEach(client => {
    bounds.extend(new google.maps.LatLng(client.lat, client.lng));

    var marker = new google.maps.Marker({
        position: {lat: client.lat, lng: client.lng},
        map,
        icon: house_img_url,
    });

    var infowindow = new google.maps.InfoWindow({
        content: 'Unassigned client'
    });

    marker.addListener('click', () => {
        infowindow.open(map, marker);
    });
});

points.forEach(point => {
    bounds.extend(new google.maps.LatLng(point.lat, point.lng));

    var marker = new google.maps.Marker({
        position: {lat: point.lat, lng: point.lng},
        map,
    });

    if(point.assigned_clients.length === 1) {
        var content = '<p>1 client</p>';
    } else {
        var content = `<p>${point.assigned_clients.length} clients</p>`;
    }

    var client_markers = point.assigned_clients.map(client => {
        bounds.extend(new google.maps.LatLng(client.lat, client.lng));

        var client_marker = new google.maps.Marker({
            position: {lat: client.lat, lng: client.lng},
            map,
        });
        client_marker.setVisible(false);
        return client_marker;
    });

    var infowindow = new google.maps.InfoWindow({content});

    marker.addListener('click', () => {
        infowindow.open(map, marker);
        var new_visible = !client_markers[0].getVisible();
        client_markers.forEach(marker => marker.setVisible(new_visible));
    });
});

map.fitBounds(bounds);
map.panToBounds(bounds);
