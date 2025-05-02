let map;
let startMarker;
let endMarker;
let routeLine;

// Initialize the map
function initMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found');
        return;
    }

    try {
        // Create the map with a default view
        map = L.map('map').setView([0, 0], 2);

        // Add the OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Check for geolocation support
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Center the map on the user's location
                const userLocation = [lat, lon];
                map.setView(userLocation, 8);

                // Add a marker for the user's location
                L.marker(userLocation).addTo(map).bindPopup('You are here').openPopup();
            }, function(error) {
                console.warn("Geolocation failed:", error);
            });
        } else {
            console.warn("Geolocation is not supported by this browser.");
        }

        console.log('Map initialized successfully');
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

// Make sure the DOM is fully loaded before initializing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
} else {
    initMap();
}

// Handle form submission
document.getElementById('transportForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    // Send the form data to the server
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data);

        // For now, we'll just show markers for start and end points
        // In a real implementation, you would use a routing service to get the actual route

        // Clear existing markers and route
        if (startMarker) map.removeLayer(startMarker);
        if (endMarker) map.removeLayer(endMarker);
        if (routeLine) map.removeLayer(routeLine);

        // Add markers for start and end points
        // Note: In a real implementation, you would need to geocode these addresses
        // For now, we'll use dummy coordinates
        const startCoords = [0, 0];  // Replace with actual geocoding
        const endCoords = [1, 1];    // Replace with actual geocoding

        startMarker = L.marker(startCoords).addTo(map)
            .bindPopup('Start: ' + data.start);

        endMarker = L.marker(endCoords).addTo(map)
            .bindPopup('End: ' + data.end);

        // Draw a simple line between points
        routeLine = L.polyline([startCoords, endCoords], {
            color: 'blue',
            weight: 3
        }).addTo(map);

        // Fit the map to show both markers
        map.fitBounds(routeLine.getBounds());
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
});