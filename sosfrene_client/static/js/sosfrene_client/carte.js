var map;

$(document).ready(function() {
    $.get("/specimens-carte/", function(response) {
        ajouterSpecimens(response.specimens);
    });
});

function ajouterSpecimens(specimens) {
    $map = $("#map");
    specimens.forEach(function(element) {
        position = new google.maps.LatLng(element.latitude, element.longitude);
        var marker = new google.maps.Marker({
            position: position,
            map: map,
            title: element.id.toString()
        });
        var infowindow = new google.maps.InfoWindow({
            content: element.etat
        });
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });
    }, this);
}

function initMap() {
    var Montreal = {lat: 45.5537692, lng: -73.7242297};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: Montreal
    });
}
