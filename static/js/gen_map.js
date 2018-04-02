var bounds = new google.maps.LatLngBounds();
var map = new google.maps.Map(document.getElementById("map_canvas"), {
    zoom: 15,
});

var clients_set = 0;
var markers = [];
var assigned_clients = [];

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

    markers.push(marker);

    if(point.assigned_clients.length === 1) {
        var content = '<p>1 client</p>';
    } else {
        var content = `<p>${point.assigned_clients.length} clients</p>`;
    }

    point.assigned_clients.forEach(client => {
        // bounds.extend(new google.maps.LatLng(client.lat, client.lng));

        // var client_marker = new google.maps.Marker({
        //     position: {lat: client.lat, lng: client.lng},
        //     map,
        //     //visible: markers[marker].visible,
        // }).setVisible(false);

        // //markers.push(client_marker);

        assigned_clients.push(client);

    });


    var infowindow = new google.maps.InfoWindow({content});


    marker.addListener('click', () => {
        
        infowindow.open(map, marker);

        // if(clients_set) {
            
        // } else {
            
        // }
        
    });
});

assigned_clients.forEach(client => {
    bounds.extend(new google.maps.LatLng(client.lat, client.lng));

        var client_marker = new google.maps.Marker({
            position: {lat: client.lat, lng: client.lng},
            map,
            //visible: markers[marker].visible,
        }).setVisible(false);

        markers.push(client_marker);
});

map.fitBounds(bounds);
map.panToBounds(bounds);
