import { map } from './map.js';

function loadRoute() {
    const origin = document.getElementById('origin');
    const destination = document.getElementById('destination');
    const freightWeight = document.getElementById('freightWeight');
    const freightSize = document.getElementById('freightSize');

    // Validation checks with interactive warnings
    if (!origin.value) {
        origin.setCustomValidity('Origin cannot be empty.');
        origin.reportValidity();
        return;
    } else {
        origin.setCustomValidity('');
    }

    if (!destination.value) {
        destination.setCustomValidity('Destination cannot be empty.');
        destination.reportValidity();
        return;
    } else {
        destination.setCustomValidity('');
    }

    if (!freightSize.value) {
        freightSize.setCustomValidity('Freight size cannot be empty.');
        freightSize.reportValidity();
        return;
    } else {
        freightSize.setCustomValidity('');
    }

    if (!freightWeight.value) {
        freightWeight.setCustomValidity('Freight weight cannot be empty.');
        freightWeight.reportValidity();
        return;
    } else {
        freightWeight.setCustomValidity('');
    }

    const formData = new FormData();
    formData.append('origin', origin.value);
    formData.append('destination', destination.value);
    formData.append('truckCheckBox', document.getElementById('truck').checked ? 'on' : '');
    formData.append('trainCheckBox', document.getElementById('train').checked ? 'on' : '');
    formData.append('shipCheckBox', document.getElementById('ship').checked ? 'on' : '');
    formData.append('airCheckBox', document.getElementById('air').checked ? 'on' : '');
    formData.append('timeImportance', document.getElementById('time-slider').value);
    formData.append('co2Importance', document.getElementById('co2-slider').value);
    formData.append('moneyImportance', document.getElementById('money-slider').value);
    formData.append('riskImportance', document.getElementById('risk-slider').value);
    formData.append('freightWeight', freightWeight.value);
    formData.append('freightSize', freightSize.value);
    console.log("Form data:", formData);

    fetch('http://localhost:5000/route', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(route => {
        console.log("Route data:", route);
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

window.loadRoute = loadRoute;