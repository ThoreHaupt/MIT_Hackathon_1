let map;
let startMarker;
let endMarker;
let routeLine;
let currentRoutes = [];
let selectedRoute = null;

// Initialize the map
function initMap() {
    // Wait for the map container to be available
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found');
        return;
    }

    try {
        // Create the map centered on a default location
        map = L.map('map').setView([0, 0], 2);

        // Add the OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

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

// Function to create a route item element
function createRouteItem(route) {
    const div = document.createElement('div');
    div.className = 'route-item';
    div.dataset.routeId = route.id;

    const header = document.createElement('div');
    header.className = 'route-header';

    const title = document.createElement('h5');
    title.className = 'route-title';
    title.textContent = `Route ${route.id}`;

    const badgesContainer = document.createElement('div');
    badgesContainer.className = 'transport-badges';

    // Create badges for each transport mode
    route.transportModes.forEach(mode => {
        const badge = document.createElement('span');
        badge.className = `transport-badge transport-${mode}`;
        badge.textContent = mode.charAt(0).toUpperCase() + mode.slice(1);
        badgesContainer.appendChild(badge);
    });

    header.appendChild(title);
    header.appendChild(badgesContainer);

    const details = document.createElement('div');
    details.className = 'route-details';

    const costDetail = createDetailElement('Cost', `$${route.cost.toFixed(2)}`);
    const timeDetail = createDetailElement('Time', `${route.time} hours`);
    const carbonDetail = createDetailElement('Carbon', `${route.carbon} kg CO₂`);

    details.appendChild(costDetail);
    details.appendChild(timeDetail);
    details.appendChild(carbonDetail);

    div.appendChild(header);
    div.appendChild(details);

    // Add click handler
    div.addEventListener('click', () => selectRoute(route));

    return div;
}

// Helper function to create detail elements
function createDetailElement(label, value) {
    const div = document.createElement('div');
    div.className = 'route-detail';

    const labelSpan = document.createElement('span');
    labelSpan.className = 'detail-label';
    labelSpan.textContent = label;

    const valueSpan = document.createElement('span');
    valueSpan.className = 'detail-value';
    valueSpan.textContent = value;

    div.appendChild(labelSpan);
    div.appendChild(valueSpan);

    return div;
}

// Function to select a route
function selectRoute(route) {
    // Remove selected class from all routes
    document.querySelectorAll('.route-item').forEach(item => {
        item.classList.remove('selected');
    });

    // Add selected class to clicked route
    const routeElement = document.querySelector(`[data-route-id="${route.id}"]`);
    if (routeElement) {
        routeElement.classList.add('selected');
    }

    // Update map
    updateMapRoute(route);

    selectedRoute = route;
}

// Function to update the map with the selected route
function updateMapRoute(route) {
    // Clear existing route
    if (routeLine) {
        map.removeLayer(routeLine);
    }

    // Draw new route with segments for different transport modes
    const segments = route.segments || [];
    segments.forEach(segment => {
        const polyline = L.polyline(segment.coordinates, {
            color: getTransportColor(segment.mode),
            weight: 3
        }).addTo(map);

        // Add a small label for the transport mode
        const midPoint = segment.coordinates[Math.floor(segment.coordinates.length / 2)];
        L.marker(midPoint, {
            icon: L.divIcon({
                className: 'transport-label',
                html: `<span class="transport-label-text">${segment.mode}</span>`
            })
        }).addTo(map);
    });

    // Fit map to route
    const bounds = L.latLngBounds(segments.flatMap(segment => segment.coordinates));
    map.fitBounds(bounds);
}

// Helper function to get color based on transport mode
function getTransportColor(mode) {
    const colors = {
        road: '#0d47a1',
        rail: '#1b5e20',
        sea: '#006064',
        air: '#880e4f'
    };
    return colors[mode] || '#000000';
}

// Function to sort routes
function sortRoutes(routes, sortBy) {
    return [...routes].sort((a, b) => {
        switch (sortBy) {
            case 'cost':
                return a.cost - b.cost;
            case 'time':
                return a.time - b.time;
            case 'carbon':
                return a.carbon - b.carbon;
            default:
                return 0;
        }
    });
}

// Function to filter routes
function filterRoutes(routes, transportMode) {
    if (transportMode === 'all') {
        return routes;
    }
    return routes.filter(route => route.transportModes.includes(transportMode));
}

// Function to update the route list
function updateRouteList() {
    const sortBy = document.getElementById('sortBy').value;
    const transportMode = document.getElementById('filterTransport').value;

    // Sort and filter routes
    let displayRoutes = sortRoutes(currentRoutes, sortBy);
    displayRoutes = filterRoutes(displayRoutes, transportMode);

    // Update the list
    const container = document.getElementById('routeAlternatives');
    container.innerHTML = '';

    displayRoutes.forEach(route => {
        container.appendChild(createRouteItem(route));
    });

    // If there was a selected route, try to reselect it
    if (selectedRoute) {
        const selectedElement = document.querySelector(`[data-route-id="${selectedRoute.id}"]`);
        if (selectedElement) {
            selectedElement.classList.add('selected');
        }
    }
}

// Add event listeners for sorting and filtering
document.getElementById('sortBy').addEventListener('change', updateRouteList);
document.getElementById('filterTransport').addEventListener('change', updateRouteList);

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

        // For demonstration, create some dummy routes with multiple transport modes
        currentRoutes = [
            {
                id: 1,
                transportModes: ['road', 'sea'],
                cost: 150,
                time: 4,
                carbon: 120,
                segments: [
                    {
                        mode: 'road',
                        coordinates: [[0, 0], [0.3, 0.3]]
                    },
                    {
                        mode: 'sea',
                        coordinates: [[0.3, 0.3], [1, 1]]
                    }
                ]
            },
            {
                id: 2,
                transportModes: ['rail', 'road'],
                cost: 200,
                time: 6,
                carbon: 80,
                segments: [
                    {
                        mode: 'rail',
                        coordinates: [[0, 0], [0.4, 0.4]]
                    },
                    {
                        mode: 'road',
                        coordinates: [[0.4, 0.4], [1, 1]]
                    }
                ]
            },
            {
                id: 3,
                transportModes: ['sea', 'road', 'rail'],
                cost: 100,
                time: 12,
                carbon: 50,
                segments: [
                    {
                        mode: 'sea',
                        coordinates: [[0, 0], [0.3, 0.3]]
                    },
                    {
                        mode: 'road',
                        coordinates: [[0.3, 0.3], [0.6, 0.6]]
                    },
                    {
                        mode: 'rail',
                        coordinates: [[0.6, 0.6], [1, 1]]
                    }
                ]
            },
            {
                id: 4,
                transportModes: ['air', 'road'],
                cost: 300,
                time: 2,
                carbon: 200,
                segments: [
                    {
                        mode: 'air',
                        coordinates: [[0, 0], [0.7, 0.7]]
                    },
                    {
                        mode: 'road',
                        coordinates: [[0.7, 0.7], [1, 1]]
                    }
                ]
            }
        ];

        // Update the route list
        updateRouteList();

        // Select the first route by default
        if (currentRoutes.length > 0) {
            selectRoute(currentRoutes[0]);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
});