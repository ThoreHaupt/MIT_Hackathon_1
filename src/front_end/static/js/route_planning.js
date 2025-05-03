import { map } from './map.js';

function loadRoute() {
    const start = document.getElementById('start');
    const destination = document.getElementById('destination');
    const freightWeight = document.getElementById('freightWeight');
    const freightSize = document.getElementById('freightSize');

    // Validation checks with interactive warnings
    if (!start.value) {
        start.setCustomValidity('Start cannot be empty.');
        start.reportValidity();
        return;
    } else {
        start.setCustomValidity('');
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
    formData.append('start', start.value);
    formData.append('destination', destination.value);
    formData.append('truckCheckBox', document.getElementById('truck').checked ? 'on' : '');
    formData.append('trainCheckBox', document.getElementById('train').checked ? 'on' : '');
    formData.append('shipCheckBox', document.getElementById('ship').checked ? 'on' : '');
    formData.append('planeCheckBox', document.getElementById('plane').checked ? 'on' : '');
    formData.append('timeImportance', document.getElementById('time-slider').value);
    formData.append('co2Importance', document.getElementById('co2-slider').value);
    formData.append('moneyImportance', document.getElementById('money-slider').value);
    formData.append('riskImportance', document.getElementById('risk-slider').value);
    formData.append('freightWeight', freightWeight.value);
    formData.append('freightSize', freightSize.value);

        fetch('http://localhost:5000/route', {
            method: 'POST',
            body: formData
        })
    .then(response => response.json())
    .then(data => {
        const segments = data.route_segments;
        const typeColors = {
            "Truck": "yellow",
            "Train": "green",
            "Ship": "navy",
            "Plane": "red"
        };

        // Clear existing layers from the map
        map.eachLayer(layer => {
            if (!layer._url) { // Keep the tile layer
                map.removeLayer(layer);
            }
        });

        // Combine consecutive segments of the same type
        const combinedSegments = [];
        let currentSegment = null;

        segments.forEach(segment => {
            if (currentSegment && currentSegment.type === segment.type) {
            // Extend the current segment
            currentSegment.path = currentSegment.path.concat(segment.path.slice(1));
            currentSegment.distance += segment.distance;
            currentSegment.duration += segment.duration;
            currentSegment.cost += segment.cost;
            currentSegment.co2_emissions += segment.co2_emissions;
            } else {
            // Start a new segment
            if (currentSegment) {
                combinedSegments.push(currentSegment);
            }
            currentSegment = { ...segment };
            }
        });

        // Push the last segment
        if (currentSegment) {
            combinedSegments.push(currentSegment);
        }

        // Draw each combined segment with color by type
        combinedSegments.forEach(segment => {
            const color = typeColors[segment.type] || 'gray';
            const hours = Math.floor(segment.duration / 3600);
            const minutes = Math.floor((segment.duration % 3600) / 60);
            const popupContent = `
            <strong>Type:</strong> ${segment.type}<br>
            <strong>Distance:</strong> ${(segment.distance / 1000)} km<br>
            <strong>Duration:</strong> ${hours} hours ${minutes} minutes<br>
            <strong>Cost:</strong> ${segment.cost}$<br>
            <strong>CO2 Equivalent:</strong> ${segment.co2_emissions} kg
            `;
            L.polyline(segment.path, { color: color, weight: 5 }).addTo(map)
            .bindPopup(popupContent);
        });

        // Add markers at start and end
        L.marker(segments[0].path[0]).addTo(map).bindPopup("Start").openPopup();
        L.marker(segments[segments.length - 1].path[1]).addTo(map).bindPopup("Destination");

        // Adjust map view to fit all segments
        const allCoordinates = segments.flatMap(segment => segment.path);
        const bounds = L.latLngBounds(allCoordinates);
        map.fitBounds(bounds);
    })
    .catch(error => console.error('Error fetching route:', error));
}

function loadTrafficIssues() {
    const active = document.getElementById('trafficIssues').checked;
    // Remove traffic issues markers
    map.eachLayer(layer => {
        if (layer.options && layer.options.icon && layer.options.icon.options.iconUrl === 'static/resources/traffic_issue.png') {
            map.removeLayer(layer);
        }
    });
    if (!active) {
        return;
    }
    // Fetch traffic issues from the server
    fetch('http://localhost:5000/traffic_issues_request', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            // Add traffic issues markers
            const traffic_issue_icon = L.icon({
                iconUrl: 'static/resources/traffic_issue.png',
                iconSize: [30, 30],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
            });
            data.forEach(issue => {
                L.marker([issue.latitude, issue.longitude], { icon: traffic_issue_icon })
                    .addTo(map)
                    .bindPopup(`Traffic Issue: ${issue.description}`);
            });
        })
        .catch(error => console.error('Error fetching traffic issues:', error));
}
function loadConstructionSites() {
    const active = document.getElementById('constructionSites').checked;
    // Remove construction sites markers
    map.eachLayer(layer => {
        if (layer.options && layer.options.icon && layer.options.icon.options.iconUrl === 'static/resources/construction_site.png') {
            map.removeLayer(layer);
        }
    });
    if (!active) {
        return;
    }
    // Fetch construction sites from the server
    fetch('http://localhost:5000/construction_sites_request', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            // Add construction sites markers
            const construction_site_icon = L.icon({
                iconUrl: 'static/resources/construction_site.png',
                iconSize: [30, 30],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
            });
            data.forEach(site => {
                L.marker([site.latitude, site.longitude], { icon: construction_site_icon })
                    .addTo(map)
                    .bindPopup(`Construction Site: ${site.description}`);
            });
        })
        .catch(error => console.error('Error fetching construction sites:', error));
}


window.loadRoute = loadRoute;
window.loadTrafficIssues = loadTrafficIssues;
window.loadConstructionSites = loadConstructionSites;