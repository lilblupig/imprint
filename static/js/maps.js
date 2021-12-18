/*
Google Maps API - displays a map of the regions
*/

const mapCentres = {
    "": { lat: 51.00656544855768, lng: -2.195737342140075 },
    "theCommons": { lat: 51.00620066480081, lng: -2.197877878967923 },
    "townHall": { lat: 51.00581753496691, lng: -2.197173526829836 },
    "angelSquare": { lat: 51.006356916697335, lng: -2.1941698786790353 },
    "goldHill": { lat: 51.00498475545027, lng: -2.197248439316768 },
    "parkWalk": { lat: 51.004191492440924, lng: -2.200240821966139 },
    "castleHill": { lat: 51.00508080897789, lng: -2.2029776482922645 },
    "bimport": { lat: 51.00605480276046, lng: -2.199650086173893 },
};

function initMap() {
    // Produces the map, determines initial zoom level and map center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 17,
        center:  mapCentres["parkWalk"],
      });

    // Renders a polygon of each region on the map
    // Polygon co-ordinates stored in static/js/map_polygons.js
    const mapPolygon = new google.maps.Polygon({
        paths: parkWalk,
        strokeColor: "#fbb13c",
        strokeOpacity: 0.5,
        strokeWeight: 1,
        fillColor: "#fbb13c",
        fillOpacity: 0.35,
    });

    mapPolygon.setMap(map);

}