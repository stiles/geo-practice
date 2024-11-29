// Filter countries by name
function filterCountries() {
    const filterValue = document.getElementById("filter-input").value.toLowerCase();
    const gridItems = document.querySelectorAll(".grid-item");

    gridItems.forEach(item => {
        const countryName = item.getAttribute("data-name").toLowerCase();
        if (countryName.includes(filterValue)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    mapboxgl.accessToken = 'pk.eyJ1Ijoic3RpbGVzIiwiYSI6ImNsd3Rpc3V2aTAzeXUydm9sMHdoN210b2oifQ.66AJmPYxe2ixku1o7Rwdlg';

    // Get latitude and longitude from the map container attributes
    const mapContainer = document.getElementById("map");
    const mapLat = parseFloat(mapContainer.getAttribute("data-lat"));
    const mapLon = parseFloat(mapContainer.getAttribute("data-lon"));

    // Initialize the Mapbox map
    const map = new mapboxgl.Map({
        container: 'map', // ID of the map container
        style: 'mapbox://styles/stiles/cm42y7gwu00up01rdhqqxam75', // Map style
        center: [mapLon, mapLat], // Center on the country
        zoom: 2, // Initial zoom level
        minZoom: 4, // Minimum zoom level
        maxZoom: 10, // Maximum zoom level
    });

    // Add a marker at the country's location
    new mapboxgl.Marker()
        .setLngLat([mapLon, mapLat])
        .addTo(map);

    // Remove compass controls and retain zoom buttons
    map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-left');
});