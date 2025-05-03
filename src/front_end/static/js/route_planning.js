

function loadRoute() {
    const formData = new FormData();
    formData.append('origin', document.getElementById('origin').value);
    formData.append('destination', document.getElementById('destination').value);
    formData.append('truckCheckBox', document.getElementById('truck').checked ? 'on' : '');
    formData.append('trainCheckBox', document.getElementById('train').checked ? 'on' : '');
    formData.append('shipCheckBox', document.getElementById('ship').checked ? 'on' : '');
    formData.append('airCheckBox', document.getElementById('air').checked ? 'on' : '');
    formData.append('timeImportance', document.getElementById('time-slider').value);
    formData.append('co2Importance', document.getElementById('co2-slider').value);
    formData.append('moneyImportance', document.getElementById('money-slider').value);
    formData.append('riskImportance', document.getElementById('risk-slider').value);
    formData.append('freightWeight', document.getElementById('freightWeight').value);
    formData.append('freightSize', document.getElementById('freightSize').value);

    fetch('http://localhost:5000/route', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(route => {
        const segments = route.segments;
        const modeColors = {
            "Truck": "blue",
            "Train": "green",
            "Ship": "navy",
            "Air": "red"
        };

        // Clear existing layers from the map
        map.eachLayer(layer => {
            if (!layer._url) { // Keep the tile layer
                map.removeLayer(layer);
            }
        });

        // Draw each segment with color by type
        segments.forEach(segment => {
            const color = modeColors[segment.type] || 'gray';
            L.polyline(segment.path, { color: color, weight: 5 }).addTo(map)
                .bindPopup(`Mode: ${segment.type}`);
        });

        // Add markers at start and end
        L.marker(segments[0].path[0]).addTo(map).bindPopup("Origin").openPopup();
        L.marker(segments[segments.length - 1].path[1]).addTo(map).bindPopup("Destination");

        // Adjust map view to fit all segments
        const allCoordinates = segments.flatMap(segment => segment.path);
        const bounds = L.latLngBounds(allCoordinates);
        map.fitBounds(bounds);
    })
    .catch(error => console.error('Error fetching route:', error));
}