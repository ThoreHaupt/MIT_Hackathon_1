
export let map;
function initMap() {
    map = L.map('map', {zoomControl: false}).setView([42.36018610476105, -71.09414927401798], 7); // Default to MIT
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Set view to user's location if available
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            map.setView([lat, lon], 10); // Center map on user's location
            L.marker([lat, lon]).addTo(map).openPopup();
        }, function(error) {
            console.error("Geolocation failed:", error);
        });
    } else {
        console.warn("Geolocation is not supported by this browser.");
    }
}

function useLocation(buttonId, inputName) {
    // Add event listener to the button
    document.getElementById(buttonId).addEventListener('click', function() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Fill input with coordinates (you can reverse geocode if needed)
                document.querySelector(`input[name="${inputName}"]`).value = `${lat}, ${lon}`;

                // Center map on user's location
                const userLocation = [lat, lon];
                map.setView(userLocation, 10);
                L.marker(userLocation).addTo(map).openPopup();
            }, function(error) {
                console.error("Geolocation failed:", error);
                alert("Unable to retrieve your location. Please try again.");
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });
}

initMap();
// Add event listeners for location buttons
useLocation('use-location-start', 'start');
useLocation('use-location-destination', 'destination');