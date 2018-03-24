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

    marker.addListener('click', marker => {
        infowindow.open(map, marker);
    });
});

var heatmap_points = points.map(point => {
    bounds.extend(new google.maps.LatLng(point.lat, point.lng));

    var marker = new google.maps.Marker({
        position: {lat: point.lat, lng: point.lng},
        map,
    });

    var infowindow = new google.maps.InfoWindow({
        content: `<p>${point.num_assigned_clients} clients </p>`
    });

    marker.addListener('click', marker => {
        infowindow.open(map, marker);
    });

    return {
        location: new google.maps.LatLng(point.lat, point.lng),
        weight: point.num_assigned_clients,
    };
});

new google.maps.visualization.HeatmapLayer({
    data: heatmap_points,
    dissipating: false,
    map
});

map.fitBounds(bounds);
map.panToBounds(bounds);
