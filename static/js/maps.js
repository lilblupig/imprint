/*
Google Maps API - displays a map of the regions
*/

const mapCentres = {
    "": { lng: -2.195737342140075, lat: 51.00656544855768 },
    "angelSquare": { lng: -2.1941698786790353, lat: 51.006356916697335 },
    "rTwo": { lng: -2.60000, lat: 51.45000 },
};

function initMap() {
    // Produces the map, determines initial zoom level and map center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 17,
        center:  mapCentres["angelSquare"],
      });

    // Renders a polygon of each region on the map
    // Polygon co-ordinates stored in static/js/map_polygons.js
    const mapPolygon = new google.maps.Polygon({
        paths: angelSquare,
        strokeColor: "#fbb13c",
        strokeOpacity: 0.5,
        strokeWeight: 1,
        fillColor: "#fbb13c",
        fillOpacity: 0.35,
    });

    mapPolygon.setMap(map);

}