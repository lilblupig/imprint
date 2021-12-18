/*
Google Maps API - displays a map of the regions
*/

function initMap() {
    // Produces the map, determines initial zoom level and map center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: { lat: -34.397, lng: 150.644 },
      });

}