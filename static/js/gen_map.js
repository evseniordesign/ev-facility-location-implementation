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

    var infowindow = new google.maps.InfoWindow({content});

    marker.addListener('click', () => {
        infowindow.open(map, marker);
        // setvisible all the clients tied to a facility
        // Take all markers for facility and set marker.setVisible(true). If true, then set false.
    });
});

map.fitBounds(bounds);
map.panToBounds(bounds);
