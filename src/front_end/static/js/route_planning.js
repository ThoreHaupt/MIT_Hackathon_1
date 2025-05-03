import { map } from './map.js';

function fillRouteDetails(route) {
    console.log(route);
    const routeDetailsDiv = document.getElementById('route-details');
    routeDetailsDiv.innerHTML = '';
    let duration = 0;
    let distance = 0;
    let cost = 0;
    let co2_emissions = 0;
    let contains_truck = false;
    let contains_train = false;
    let contains_ship = false;
    let contains_plane = false;
    route.forEach(segment => {
        if (segment.type === 'Truck') {
            contains_truck = true;
        } else if (segment.type === 'Train') {
            contains_train = true;
        } else if (segment.type === 'Ship') {
            contains_ship = true;
        } else if (segment.type === 'Plane') {
            contains_plane = true;
        } 
        duration += segment.duration;
        distance += segment.distance;
        cost += segment.cost;
        co2_emissions += segment.co2_emissions;
    });
    const hours = Math.floor(duration / 3600);
    const minutes = Math.floor((duration % 3600) / 60);
    let details = `
        <div class="mt-4 bg-white/90 shadow-lg rounded-xl p-4 h-48">
        <p><strong>Total Duration:</strong> ${hours} hours ${minutes} minutes</p>
        <p><strong>Total Distance:</strong> ${(distance / 1000).toFixed(2)} km</p>
        <p><strong>Total Cost:</strong> ${cost}$</p>
        <p><strong>Total CO2 Equivalent:</strong> ${co2_emissions} kg</p>
        <div class="flex space-x-2">
    `;
    if (contains_truck) {
        details += `
        <svg viewBox="0 0 22 20" class="h-12 mt-2 mb-2" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M8.52832 16.826C8.53464 17.7132 8.01843 18.5166 7.22106 18.8607C6.42369 19.2047 5.50274 19.0213 4.88882 18.3962C4.27491 17.7712 4.08935 16.828 4.41891 16.0077C4.74847 15.1873 5.52803 14.652 6.39307 14.652C6.95731 14.6499 7.49925 14.8777 7.89969 15.2854C8.30013 15.6931 8.52625 16.2473 8.52832 16.826V16.826Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M18.7015 16.826C18.7078 17.7132 18.1916 18.5166 17.3942 18.8607C16.5969 19.2047 15.6759 19.0213 15.062 18.3962C14.4481 17.7712 14.2625 16.828 14.5921 16.0077C14.9216 15.1873 15.7012 14.652 16.5662 14.652C17.1305 14.6499 17.6724 14.8777 18.0728 15.2854C18.4733 15.6931 18.6994 16.2473 18.7015 16.826Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M14.1804 17.576C14.5946 17.576 14.9304 17.2403 14.9304 16.826C14.9304 16.4118 14.5946 16.076 14.1804 16.076V17.576ZM8.5254 16.076C8.11119 16.076 7.7754 16.4118 7.7754 16.826C7.7754 17.2403 8.11119 17.576 8.5254 17.576V16.076ZM13.4304 16.826C13.4304 17.2403 13.7662 17.576 14.1804 17.576C14.5946 17.576 14.9304 17.2403 14.9304 16.826H13.4304ZM14.9304 11.559C14.9304 11.1448 14.5946 10.809 14.1804 10.809C13.7662 10.809 13.4304 11.1448 13.4304 11.559H14.9304ZM14.1804 16.076C13.7662 16.076 13.4304 16.4118 13.4304 16.826C13.4304 17.2403 13.7662 17.576 14.1804 17.576V16.076ZM14.43 17.576C14.8442 17.576 15.18 17.2403 15.18 16.826C15.18 16.4118 14.8442 16.076 14.43 16.076V17.576ZM18.6972 16.0761C18.283 16.0779 17.9487 16.4151 17.9505 16.8293C17.9523 17.2435 18.2896 17.5779 18.7038 17.576L18.6972 16.0761ZM20.9625 14.485L21.7125 14.4816C21.7123 14.4384 21.7084 14.3954 21.7008 14.3529L20.9625 14.485ZM21.1772 11.4269C21.1042 11.0192 20.7146 10.7478 20.3068 10.8208C19.8991 10.8937 19.6277 11.2834 19.7007 11.6912L21.1772 11.4269ZM14.1794 6.12705C13.7652 6.12705 13.4294 6.46283 13.4294 6.87705C13.4294 7.29126 13.7652 7.62705 14.1794 7.62705V6.12705ZM17.7587 6.87705V7.62705C17.7637 7.62705 17.7688 7.627 17.7739 7.62689L17.7587 6.87705ZM19.3783 7.55055L19.9178 7.02951L19.9178 7.02951L19.3783 7.55055ZM20.0197 9.21805L19.27 9.19669C19.2685 9.24804 19.2723 9.2994 19.2814 9.34996L20.0197 9.21805ZM19.6996 11.691C19.7725 12.0987 20.1621 12.3702 20.5699 12.2974C20.9776 12.2245 21.2491 11.8349 21.1763 11.4271L19.6996 11.691ZM14.9284 6.87705C14.9284 6.46283 14.5927 6.12705 14.1784 6.12705C13.7642 6.12705 13.4284 6.46283 13.4284 6.87705H14.9284ZM13.4284 11.559C13.4284 11.9733 13.7642 12.309 14.1784 12.309C14.5927 12.309 14.9284 11.9733 14.9284 11.559H13.4284ZM13.4284 6.87705C13.4284 7.29126 13.7642 7.62705 14.1784 7.62705C14.5927 7.62705 14.9284 7.29126 14.9284 6.87705H13.4284ZM14.1784 6.07705L14.9285 6.07705L14.9284 6.07167L14.1784 6.07705ZM13.1137 5.00005L13.1137 5.75006L13.1187 5.75003L13.1137 5.00005ZM3.50512 5.00005L3.498 5.75005H3.50512V5.00005ZM2.75423 5.31075L2.22207 4.78225L2.22207 4.78225L2.75423 5.31075ZM2.4375 6.07505L1.6875 6.06834V6.07505H2.4375ZM2.4375 15.75L1.68747 15.75L1.68753 15.7568L2.4375 15.75ZM2.75423 16.5143L3.28638 15.9858L3.28638 15.9858L2.75423 16.5143ZM3.50512 16.825L3.50512 16.075L3.498 16.0751L3.50512 16.825ZM4.25783 17.575C4.67204 17.575 5.00783 17.2393 5.00783 16.825C5.00783 16.4108 4.67204 16.075 4.25783 16.075V17.575ZM14.1804 10.809C13.7662 10.809 13.4304 11.1448 13.4304 11.559C13.4304 11.9733 13.7662 12.309 14.1804 12.309V10.809ZM20.4399 12.309C20.8541 12.309 21.1899 11.9733 21.1899 11.559C21.1899 11.1448 20.8541 10.809 20.4399 10.809V12.309ZM14.1804 16.076H8.5254V17.576H14.1804V16.076ZM14.9304 16.826V11.559H13.4304V16.826H14.9304ZM14.1804 17.576H14.43V16.076H14.1804V17.576ZM18.7038 17.576C19.5117 17.5725 20.281 17.2397 20.8437 16.6573L19.765 15.615C19.4792 15.9108 19.0947 16.0743 18.6972 16.0761L18.7038 17.576ZM20.8437 16.6573C21.4058 16.0756 21.7162 15.2926 21.7125 14.4816L20.2125 14.4885C20.2145 14.9137 20.0514 15.3186 19.765 15.615L20.8437 16.6573ZM21.7008 14.3529L21.1772 11.4269L19.7007 11.6912L20.2242 14.6172L21.7008 14.3529ZM14.1794 7.62705H17.7587V6.12705H14.1794V7.62705ZM17.7739 7.62689C18.1691 7.61888 18.5544 7.7771 18.8389 8.07158L19.9178 7.02951C19.3477 6.43922 18.5622 6.1106 17.7434 6.1272L17.7739 7.62689ZM18.8389 8.07158C19.124 8.36679 19.282 8.77315 19.27 9.19669L20.7694 9.2394C20.7928 8.41808 20.4872 7.61907 19.9178 7.02951L18.8389 8.07158ZM19.2814 9.34996L19.6996 11.691L21.1763 11.4271L20.758 9.08613L19.2814 9.34996ZM13.4284 6.87705V11.559H14.9284V6.87705H13.4284ZM14.9284 6.87705V6.07705H13.4284V6.87705H14.9284ZM14.9284 6.07167C14.9213 5.07677 14.1245 4.24331 13.1088 4.25006L13.1187 5.75003C13.2708 5.74902 13.427 5.87963 13.4285 6.08242L14.9284 6.07167ZM13.1137 4.25005H3.50512V5.75005H13.1137V4.25005ZM3.51225 4.25008C3.02654 4.24547 2.5628 4.43917 2.22207 4.78225L3.28638 5.83925C3.3461 5.77912 3.42257 5.7493 3.498 5.75001L3.51225 4.25008ZM2.22207 4.78225C1.88199 5.12468 1.69183 5.58769 1.68753 6.06834L3.18747 6.08175C3.18832 5.98687 3.22602 5.90003 3.28638 5.83925L2.22207 4.78225ZM1.6875 6.07505V15.75H3.1875V6.07505H1.6875ZM1.68753 15.7568C1.69183 16.2374 1.88199 16.7004 2.22207 17.0428L3.28638 15.9858C3.22602 15.9251 3.18832 15.8382 3.18747 15.7433L1.68753 15.7568ZM2.22207 17.0428C2.5628 17.3859 3.02654 17.5796 3.51225 17.575L3.498 16.0751C3.42257 16.0758 3.3461 16.046 3.28638 15.9858L2.22207 17.0428ZM3.50512 17.575H4.25783V16.075H3.50512V17.575ZM14.1804 12.309H20.4399V10.809H14.1804V12.309Z" fill="#000000"></path> </g></svg>
        `;
    }
    if (contains_train) {
        console.log('contains train');
        details += `
        <svg viewBox="0 0 22 20" class="h-12 mt-2 ml-6 mb-2" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M5 11H19M9 18L6 21M15 18L18 21M12 11V4M8 15H8.01M16 15H16.01M8.2 18H15.8C16.9201 18 17.4802 18 17.908 17.782C18.2843 17.5903 18.5903 17.2843 18.782 16.908C19 16.4802 19 15.9201 19 14.8V6.2C19 5.0799 19 4.51984 18.782 4.09202C18.5903 3.71569 18.2843 3.40973 17.908 3.21799C17.4802 3 16.9201 3 15.8 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.07989 5 6.2V14.8C5 15.9201 5 16.4802 5.21799 16.908C5.40973 17.2843 5.71569 17.5903 6.09202 17.782C6.51984 18 7.07989 18 8.2 18Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
        `;
    }
    if (contains_ship) {
        details += `
        <svg viewBox="0 0 22 20" class="h-12 mt-2 ml-12 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m3 17 .756.378a3 3 0 0 0 2.523.074l1.04-.446a3 3 0 0 1 2.363 0l1.04.446a3 3 0 0 0 2.523-.074l.413-.207a3 3 0 0 1 2.684 0l.547.273a3 3 0 0 0 2.29.163L21 17M5 14.5 4 10h4m10 4.5 2.5-4.5h-8.245H13.5m0 0-.721-3H8v3m5.5 0H8m3 3h.1M10 4.5l-.2-.2a2 2 0 0 0-1.899-.525l-.336.084a2 2 0 0 1-1.118-.043L5.5 3.5"></path> </g></svg>
        `;
    }
    if (contains_plane) {
        details += `
        <svg fill="#000000" viewBox="0 0 30 30" class="h-12 mt-2 ml-12 mb-2" id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <defs> <style> .cls-1 { fill: none; } </style> </defs> <path d="M28.5845,14.585l-3.12-1.8721A4.9951,4.9951,0,0,0,22.8921,12H7.7808L7.16,9.5151A1.9975,1.9975,0,0,0,5.2192,8H4a2.0023,2.0023,0,0,0-2,2v7a3.0033,3.0033,0,0,0,3,3h7v6a2.0023,2.0023,0,0,0,2,2h1.3071A2.0086,2.0086,0,0,0,17.18,26.7021L19.6929,20h7.3916a2.9152,2.9152,0,0,0,1.5-5.415ZM27.0845,18H18.3071l-3,8H14V18H5a1.0009,1.0009,0,0,1-1-1V10H5.2192l1,4H10v2h2V14h3v2h2V14h3v2h2V14h.8921a2.9977,2.9977,0,0,1,1.5434.4277l3.12,1.8721a.9154.9154,0,0,1-.4712,1.7Z" transform="translate(0 0)"></path> <path d="M14,4h1.3228l2.4,6h2.1545L17.18,3.2573A1.9906,1.9906,0,0,0,15.3228,2H14a2.0023,2.0023,0,0,0-2,2v6h2Z" transform="translate(0 0)"></path> <rect id="_Transparent_Rectangle_" data-name="<Transparent Rectangle>" class="cls-1" width="32" height="32"></rect> </g></svg>
        `;
    }
    details += `</div></div></div>`;
    routeDetailsDiv.innerHTML = details;
    routeDetailsDiv.style.display = 'block';
}

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
        L.marker(segments[0].path[0]).addTo(map).bindPopup("Start");
        L.marker(segments[segments.length - 1].path[1]).addTo(map).bindPopup("Destination");

        // Adjust map view to fit all segments
        const allCoordinates = segments.flatMap(segment => segment.path);
        const bounds = L.latLngBounds(allCoordinates);
        map.fitBounds(bounds);

        fillRouteDetails(segments);
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

    // Show preloaded traffic issues markers
    preloadedTrafficIssues.forEach(marker => {
        marker.addTo(map);
    });
}

// Preload traffic issues markers at startup
const preloadedTrafficIssues = [];
fetch('http://localhost:5000/traffic_issues_request', {
    method: 'POST',
})
    .then(response => response.json())
    .then(data => {
        const traffic_issue_icon = L.icon({
            iconUrl: 'static/resources/traffic_issue.png',
            iconSize: [30, 30],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
        });
        data.forEach(issue => {
            const marker = L.marker([issue.latitude, issue.longitude], { icon: traffic_issue_icon })
                .bindPopup(`Traffic Issue: ${issue.description}`);
            preloadedTrafficIssues.push(marker);
        });
    })
    .catch(error => console.error('Error preloading traffic issues:', error));
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

    // Show preloaded construction sites markers
    preloadedConstructionSites.forEach(marker => {
        marker.addTo(map);
    });
}

// Preload construction sites markers at startup
const preloadedConstructionSites = [];
fetch('http://localhost:5000/construction_sites_request', {
    method: 'POST',
})
    .then(response => response.json())
    .then(data => {
        const construction_site_icon = L.icon({
            iconUrl: 'static/resources/construction_site.png',
            iconSize: [30, 30],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
        });
        data.forEach(site => {
            const marker = L.marker([site.latitude, site.longitude], { icon: construction_site_icon })
                .bindPopup(`Construction Site: ${site.description}`);
            preloadedConstructionSites.push(marker);
        });
    })
    .catch(error => console.error('Error preloading construction sites:', error));


window.loadRoute = loadRoute;
window.loadTrafficIssues = loadTrafficIssues;
window.loadConstructionSites = loadConstructionSites;