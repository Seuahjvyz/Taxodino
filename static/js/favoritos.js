// Configuración
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Cargar favoritos al iniciar
document.addEventListener('DOMContentLoaded', function() {
    cargarFavoritos();
});

async function cargarFavoritos() {
    const grid = document.getElementById('dinosaursGrid');
    
    // Obtener favoritos del localStorage
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (favorites.length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-heart-broken"></i>
                <h3>No tienes favoritos aún</h3>
                <p>Explora dinosaurios y guarda tus favoritos ❤️</p>
                <a href="/" style="display: inline-block; margin-top: 1rem; color: #E67E22;">Volver al inicio</a>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-dragon"></i><p>Cargando tus favoritos...</p></div>';
    
    try {
        // Cargar cada dinosaurio por ID
        const dinosaurios = [];
        for (const dinoId of favorites) {
            const response = await fetch(`${API_BASE_URL}/dinosaurs/${dinoId}`);
            if (response.ok) {
                const data = await response.json();
                dinosaurios.push(data);
            }
        }
        
        renderDinosaurios(dinosaurios);
    } catch (error) {
        console.error('Error cargando favoritos:', error);
        grid.innerHTML = '<div class="no-results"><i class="fas fa-exclamation-triangle"></i><h3>Error al cargar</h3><p>Intenta nuevamente más tarde</p></div>';
    }
}

function renderDinosaurios(dinosaurios) {
    const grid = document.getElementById('dinosaursGrid');
    
    if (dinosaurios.length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-heart-broken"></i>
                <h3>No se encontraron dinosaurios</h3>
                <p>Prueba con otra búsqueda</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = dinosaurios.map(dino => `
        <div class="dino-card" onclick="verDetalle(${dino.id})">
            <img class="dino-image" src="${dino.imagen_url || 'https://placehold.co/600x400/2D4A22/white?text=Dinosaurio'}" alt="${dino.nombre}">
            <div class="dino-info">
                <h3 class="dino-name">${dino.nombre}</h3>
                <p class="dino-scientific">${dino.nombre_cientifico || ''}</p>
                <div class="dino-details">
                    ${dino.dieta ? `<span class="dino-badge"><i class="fas fa-drumstick-bite"></i> ${dino.dieta}</span>` : ''}
                    ${dino.periodo ? `<span class="dino-badge"><i class="fas fa-clock"></i> ${dino.periodo}</span>` : ''}
                </div>
                <p class="dino-description">${(dino.descripcion || '').substring(0, 120)}...</p>
                <div class="dino-footer">
                    <button class="favorite-btn active" onclick="event.stopPropagation(); toggleFavorite(${dino.id}, this)">
                        <i class="fas fa-heart"></i>
                    </button>
                    <a href="#" class="dino-link" onclick="event.stopPropagation(); verDetalle(${dino.id})">
                        Ver más <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
    `).join('');
}

function verDetalle(id) {
    window.location.href = `/dinosaurio/${id}`;
}

function toggleFavorite(dinoId, button) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (favorites.includes(dinoId)) {
        favorites = favorites.filter(id => id !== dinoId);
        button.classList.remove('active');
        // Recargar la página para actualizar la lista
        cargarFavoritos();
    } else {
        favorites.push(dinoId);
        button.classList.add('active');
    }
    
    localStorage.setItem('favorites', JSON.stringify(favorites));
}