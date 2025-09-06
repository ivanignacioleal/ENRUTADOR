// app.js

let map;
let taskMarkers = [];

function initializeMap() {
    map = L.map('map').setView([-25.27599149, -65.4850453], 13);  // Punto de partida en Salta
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
}

function clearMap() {
    taskMarkers.forEach(marker => map.removeLayer(marker));
    taskMarkers = [];
}

function loadTasksOnMap(tasks) {
    clearMap();
    tasks.forEach(task => {
        const coords = [parseFloat(task[2]), parseFloat(task[3])];  // Parseamos las coordenadas
        const marker = L.marker(coords).addTo(map)
            .bindPopup(`<b>${task[1]}</b><br>Coordenadas: (${coords[0]}, ${coords[1]})`);
        taskMarkers.push(marker);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initializeMap();  // Inicializar el mapa al cargar la página

    fetch('/tasks')  // Ruta que entrega las tareas desde el backend
        .then(response => response.json())
        .then(tasks => {
            loadTasksOnMap(tasks);  // Cargar las tareas en el mapa
        })
        .catch(err => {
            console.error('Error al cargar tareas:', err);
        });
});
