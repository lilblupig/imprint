/*
Google Maps API - displays a map of the regions
*/

/* Define global variables */
let chosenValue = document.getElementById("location-choice");
let area;

/* See if a filter is applied and set area */
if (chosenValue) {
    area = chosenValue.innerHTML;
} else {
    area = chosenValue;
}

/* Set map centres for chosen locations */
const mapCentres = {
    null: { lat: 51.00656544855768, lng: -2.195737342140075 },
    "The Commons": { lat: 51.00620066480081, lng: -2.197877878967923 },
    "Town Hall": { lat: 51.00581753496691, lng: -2.197173526829836 },
    "Angel Square": { lat: 51.006356916697335, lng: -2.1941698786790353 },
    "Gold Hill": { lat: 51.00498475545027, lng: -2.197248439316768 },
    "Park Walk": { lat: 51.004191492440924, lng: -2.200240821966139 },
    "Castle Hill": { lat: 51.00508080897789, lng: -2.2029776482922645 },
    "Bimport": { lat: 51.00605480276046, lng: -2.199650086173893 },
    "Other": { lat: 51.00656544855768, lng: -2.195737342140075 },
};

/* Translate HTML value to variable for polygon */
const mapAreas = {
    null: placeholderMap,
    "The Commons": theCommons,
    "Town Hall": townHall,
    "Angel Square": angelSquare,
    "Gold Hill": goldHill,
    "Park Walk": parkWalk,
    "Castle Hill": castleHill,
    "Bimport": bimport,
    "Other": "",
};

/* Google Maps API call */
function initMap() {
    // Produces the map, determines initial zoom level and map center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 16,
        center:  mapCentres[area],
    });

    // Renders a polygon of each region on the map
    // Polygon co-ordinates stored in static/js/map_polygons.js
    const mapPolygon = new google.maps.Polygon({
        paths: mapAreas[area],
        strokeColor: "#1e3c8d",
        strokeOpacity: 0.5,
        strokeWeight: 2,
        fillColor: "#fbb13c",
        fillOpacity: 0.35,
    });
    mapPolygon.setMap(map);
}