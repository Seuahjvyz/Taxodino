// ============================================
// CONFIGURACIÓN
// ============================================

const API_BASE_URL = 'http://localhost:8000/api/v1';
let worldMap = null;
let worldMapMarkers = [];
let selectedCountryMarker = null;

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dino Explorers iniciado');
    initWorldMap();
    cargarDinosaurios();
    
    // Configurar búsqueda
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', () => buscarDinosaurios(searchInput.value));
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') buscarDinosaurios(searchInput.value);
        });
    }
    
    // Configurar filtros
    const filterBtns = document.querySelectorAll('.filter-btn');
    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => filtrarPorDieta(btn.dataset.filter));
        });
    }
    
    // Configurar cierre del modal
    const modal = document.getElementById('dinoModal');
    const closeBtn = document.querySelector('.modal-close');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.classList.remove('show');
        });
    }
    
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    }
});

// ============================================
// FUNCIONES PRINCIPALES
// ============================================

async function cargarDinosaurios() {
    const grid = document.getElementById('dinosaursGrid');
    if (!grid) {
        console.error('No se encontró el elemento dinosaursGrid');
        return;
    }
    
    try {
        console.log('Cargando dinosaurios desde la API...');
        const response = await fetch(`${API_BASE_URL}/dinosaurs/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Datos recibidos:', data);
        
        if (data.data && data.data.length > 0) {
            renderDinosaurios(data.data);
            const resultsCount = document.getElementById('resultsCount');
            if (resultsCount) {
                resultsCount.textContent = `Mostrando ${data.data.length} de ${data.total} dinosaurios`;
            }
        } else {
            grid.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-dragon"></i>
                    <h3>No hay dinosaurios en la base de datos</h3>
                    <p>Ejecuta el script SQL para insertar dinosaurios de ejemplo</p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">Ejemplos: Tiranosaurio Rex, Velociraptor, Triceratops</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error cargando dinosaurios:', error);
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error de conexión</h3>
                <p>No se pudo conectar con el servidor. Asegúrate que el backend esté corriendo.</p>
                <button onclick="location.reload()" style="margin-top: 1rem; padding: 8px 20px; background: #E67E22; color: white; border: none; border-radius: 20px; cursor: pointer;">Reintentar</button>
            </div>
        `;
    }
}

async function initWorldMap() {
    const mapElement = document.getElementById('worldMap');
    const select = document.getElementById('countrySelect');

    if (!mapElement || !select || typeof L === 'undefined') {
        return;
    }

    worldMap = L.map('worldMap', {
        zoomControl: true,
        scrollWheelZoom: false
    }).setView([18, 10], 2);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; CartoDB',
        subdomains: 'abcd',
        maxZoom: 18
    }).addTo(worldMap);

    select.addEventListener('change', (event) => {
        if (event.target.value) {
            cargarDinosauriosPorPais(event.target.value);
        }
    });

    await cargarPaisesMapa();
}

async function cargarPaisesMapa() {
    try {
        const response = await fetch(`${API_BASE_URL}/geografia/paises-detalle`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const paises = await response.json();
        const select = document.getElementById('countrySelect');
        if (!select) return;

        paises.forEach((pais) => {
            const option = document.createElement('option');
            option.value = pais.clave;
            option.textContent = pais.nombre;
            select.appendChild(option);

            const marker = L.circleMarker([pais.coordenadas.lat, pais.coordenadas.lng], {
                radius: 6,
                color: '#F39C12',
                weight: 2,
                fillColor: '#FFD27D',
                fillOpacity: 0.8
            }).addTo(worldMap);

            marker.bindPopup(`<strong>${escapeHtml(pais.nombre)}</strong><br>Haz clic para explorar registros.`);
            marker.on('click', () => {
                select.value = pais.clave;
                cargarDinosauriosPorPais(pais.clave);
            });
            worldMapMarkers.push(marker);
        });
    } catch (error) {
        console.error('Error cargando países del mapa:', error);
        const status = document.getElementById('mapCountryStatus');
        if (status) {
            status.textContent = 'No se pudieron cargar los países del mapa.';
        }
    }
}

async function cargarDinosauriosPorPais(pais) {
    const list = document.getElementById('mapDinosaurList');
    const status = document.getElementById('mapCountryStatus');
    const badge = document.getElementById('mapSourceBadge');

    if (!pais || !list) return;

    list.innerHTML = '<p>Cargando dinosaurios de esta región...</p>';
    if (status) {
        status.textContent = 'Consultando registros fósiles y referencias conocidas.';
    }

    try {
        const response = await fetch(`${API_BASE_URL}/geografia/dinosaurios/${encodeURIComponent(pais)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        renderMapDinosaurios(data);
        actualizarMapaSeleccionado(data);

        if (status) {
            status.textContent = `${data.pais}: ${data.total} dinosaurio(s) localizado(s).`;
        }
        if (badge) {
            badge.textContent = data.fuente || 'Sin fuente';
        }
    } catch (error) {
        console.error('Error cargando dinosaurios por país:', error);
        list.innerHTML = '<p>No fue posible cargar los dinosaurios de esta región.</p>';
        if (badge) {
            badge.textContent = 'Error';
        }
    }
}

function actualizarMapaSeleccionado(data) {
    if (!worldMap || !data || !data.coordenadas) return;

    if (selectedCountryMarker) {
        worldMap.removeLayer(selectedCountryMarker);
    }

    selectedCountryMarker = L.marker([data.coordenadas.lat, data.coordenadas.lng]).addTo(worldMap);
    selectedCountryMarker.bindPopup(`<strong>${escapeHtml(data.pais)}</strong><br>${data.total} dinosaurio(s)`).openPopup();
    worldMap.setView([data.coordenadas.lat, data.coordenadas.lng], 4);
}

function renderMapDinosaurios(data) {
    const list = document.getElementById('mapDinosaurList');
    if (!list) return;

    if (!data.dinosaurios || data.dinosaurios.length === 0) {
        list.innerHTML = `<p>${escapeHtml(data.mensaje || `No se encontraron registros para ${data.pais}.`)}</p>`;
        return;
    }

    list.innerHTML = data.dinosaurios.map((dino) => `
        <article class="map-dino-item">
            <h5>${escapeHtml(dino.nombre || dino.nombre_cientifico || 'Dinosaurio')}</h5>
            <div class="map-dino-meta">
                ${dino.periodo ? `<span><i class="fas fa-clock"></i> ${escapeHtml(dino.periodo)}</span>` : ''}
                ${dino.dieta ? `<span><i class="fas fa-drumstick-bite"></i> ${escapeHtml(dino.dieta)}</span>` : ''}
            </div>
            <p>${escapeHtml((dino.descripcion || '').substring(0, 180))}${(dino.descripcion || '').length > 180 ? '...' : ''}</p>
        </article>
    `).join('');
}

async function buscarDinosaurios(query) {
    if (!query || !query.trim()) {
        cargarDinosaurios();
        return;
    }
    
    const grid = document.getElementById('dinosaursGrid');
    if (!grid) return;
    
    grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-dragon fa-spin"></i><p>Buscando dinosaurios...</p></div>';
    
    try {
        // CORREGIDO: usar query como parámetro correctamente
        const url = `${API_BASE_URL}/dinosaurs/search/?query=${encodeURIComponent(query.trim())}`;
        console.log('Buscando en URL:', url);
        
        const response = await fetch(url);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Resultados búsqueda:', data);
        
        if (!data.data || data.data.length === 0) {
            const mensaje = data.message || `No se encontraron dinosaurios con "${query}"`;
            grid.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <h3>No se encontraron resultados</h3>
                    <p>${mensaje}</p>
                    <p style="margin-top: 1rem;">Sugerencias: "Rex", "Raptor", "Triceratops"</p>
                </div>
            `;
            return;
        }
        
        const resultados = data.data;
        renderDinosaurios(resultados);
        
        const resultsCount = document.getElementById('resultsCount');
        if (resultsCount) {
            resultsCount.textContent = `${resultados.length} resultado(s) para "${query}"`;
        }
        
    } catch (error) {
        console.error('Error en búsqueda:', error);
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error en la búsqueda</h3>
                <p>Intenta nuevamente</p>
                <button onclick="cargarDinosaurios()" style="margin-top: 1rem; padding: 8px 20px; background: #E67E22; color: white; border: none; border-radius: 20px; cursor: pointer;">Volver a cargar</button>
            </div>
        `;
    }
}

// ============================================
// RENDERIZADO
// ============================================

function renderDinosaurios(dinosaurios) {
    const grid = document.getElementById('dinosaursGrid');
    if (!grid) return;
    
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (dinosaurios.length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-dragon"></i>
                <h3>No hay dinosaurios para mostrar</h3>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = dinosaurios.map(dino => `
        <div class="dino-card" data-id="${dino.id}" onclick="verDetalle(${dino.id})">
            <img class="dino-image" 
                 src="${dino.imagen_url || `https://placehold.co/600x400/2D4A22/white?text=${encodeURIComponent(dino.nombre || 'Dinosaurio')}`}" 
                 alt="${dino.nombre || 'Dinosaurio'}"
                 onerror="this.src='https://placehold.co/600x400/2D4A22/white?text=Dinosaurio'">
            <div class="dino-info">
                <h3 class="dino-name">${escapeHtml(dino.nombre || 'Desconocido')}</h3>
                <p class="dino-scientific">${escapeHtml(dino.nombre_cientifico || '')}</p>
                <div class="dino-details">
                    ${dino.dieta ? `<span class="dino-badge"><i class="fas fa-drumstick-bite"></i> ${escapeHtml(dino.dieta)}</span>` : ''}
                    ${dino.periodo ? `<span class="dino-badge"><i class="fas fa-clock"></i> ${escapeHtml(dino.periodo)}</span>` : ''}
                </div>
                ${renderLocationSummary(dino.ubicaciones)}
                <p class="dino-description">${escapeHtml((dino.descripcion || '').substring(0, 120))}${(dino.descripcion || '').length > 120 ? '...' : ''}</p>
                <div class="dino-footer">
                    <button class="favorite-btn ${favorites.includes(dino.id) ? 'active' : ''}" 
                            onclick="event.stopPropagation(); toggleFavorite(${dino.id}, this)">
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

// ============================================
// DETALLE DEL DINOSAURIO (MODAL)
// ============================================

async function verDetalle(id) {
    console.log('🔍 Ver detalle del dinosaurio ID:', id);
    
    const modal = document.getElementById('dinoModal');
    if (!modal) {
        console.error('Modal no encontrado');
        return;
    }
    
    // Mostrar loading
    modal.classList.add('show');
    
    // Limpiar contenido anterior
    document.getElementById('modalName').textContent = 'Cargando...';
    document.getElementById('modalScientific').textContent = '';
    document.getElementById('modalDetails').innerHTML = '<div class="loading-spinner"><i class="fas fa-dragon fa-spin"></i><p>Cargando información...</p></div>';
    document.getElementById('modalDescription').innerHTML = '';
    document.getElementById('modalSources').innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/dinosaurs/${id}`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const dino = await response.json();
        console.log('Datos del dinosaurio:', dino);
        
        // Actualizar modal con la información
        document.getElementById('modalName').textContent = dino.nombre || 'Desconocido';
        document.getElementById('modalScientific').textContent = dino.nombre_cientifico || '';
        
        // Construir detalles
        let detailsHtml = `
            <div class="modal-detail-item">
                <i class="fas fa-utensils"></i>
                <strong>Dieta:</strong> <span>${escapeHtml(dino.dieta || 'Desconocida')}</span>
            </div>
            <div class="modal-detail-item">
                <i class="fas fa-clock"></i>
                <strong>Período:</strong> <span>${escapeHtml(dino.periodo || 'Desconocido')}</span>
            </div>
        `;
        
        if (dino.longitud_metros) {
            detailsHtml += `
                <div class="modal-detail-item">
                    <i class="fas fa-ruler"></i>
                    <strong>Longitud:</strong> <span>${dino.longitud_metros} metros</span>
                </div>
            `;
        }
        
        if (dino.peso_kg) {
            detailsHtml += `
                <div class="modal-detail-item">
                    <i class="fas fa-weight-hanging"></i>
                    <strong>Peso:</strong> <span>${dino.peso_kg.toLocaleString()} kg</span>
                </div>
            `;
        }

        if (dino.ubicaciones && dino.ubicaciones.length > 0) {
            detailsHtml += `
                <div class="modal-detail-item">
                    <i class="fas fa-earth-americas"></i>
                    <strong>Dónde estuvo:</strong>
                    <span>${dino.ubicaciones.map((ubicacion) => escapeHtml(ubicacion.pais)).join(', ')}</span>
                </div>
            `;
        }
        
        document.getElementById('modalDetails').innerHTML = detailsHtml;
        
        // Descripción
        document.getElementById('modalDescription').innerHTML = `
            <h4 style="margin-top: 1rem; color: #2D4A22;"><i class="fas fa-info-circle"></i> Descripción</h4>
            <p style="line-height: 1.6;">${escapeHtml(dino.descripcion || 'No hay descripción disponible.')}</p>
        `;
        
        // Curiosidades
        let curiosidadesHtml = '';
        if (dino.curiosidades && dino.curiosidades.length > 0) {
            curiosidadesHtml = `
                <h4 style="margin-top: 1rem; color: #2D4A22;"><i class="fas fa-lightbulb"></i> Curiosidades</h4>
                <ul style="margin-top: 0.5rem; padding-left: 1.5rem;">
                    ${dino.curiosidades.map(c => `<li style="margin-bottom: 0.5rem;">${escapeHtml(c)}</li>`).join('')}
                </ul>
            `;
        }
        
        const ubicacionesHtml = dino.ubicaciones && dino.ubicaciones.length > 0
            ? `
                <h4 style="margin-top: 1rem; color: #2D4A22;"><i class="fas fa-map-marker-alt"></i> Registros geográficos</h4>
                <ul style="margin-top: 0.5rem; padding-left: 1.5rem;">
                    ${dino.ubicaciones.map((ubicacion) => `<li style="margin-bottom: 0.5rem;">${escapeHtml(ubicacion.pais)}${ubicacion.continente ? ` (${escapeHtml(ubicacion.continente)})` : ''}</li>`).join('')}
                </ul>
            `
            : '';

        document.getElementById('modalSources').innerHTML = ubicacionesHtml + curiosidadesHtml;
        
        // Imagen
        const modalImage = document.getElementById('modalImage');
        const imagenUrl = dino.imagen_url || `https://placehold.co/600x400/2D4A22/white?text=${encodeURIComponent(dino.nombre || 'Dinosaurio')}`;
        modalImage.src = imagenUrl;
        modalImage.alt = dino.nombre || 'Dinosaurio';
        modalImage.onerror = function() {
            this.src = 'https://placehold.co/600x400/2D4A22/white?text=Dinosaurio';
        };
        
        console.log('✅ Modal actualizado correctamente');
        
    } catch (error) {
        console.error('❌ Error cargando detalles:', error);
        document.getElementById('modalDetails').innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #D32F2F;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem;"></i>
                <p>Error al cargar la información del dinosaurio</p>
                <p style="font-size: 0.9rem;">${error.message}</p>
            </div>
        `;
    }
}

// ============================================
// FAVORITOS
// ============================================

function toggleFavorite(dinoId, button) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (favorites.includes(dinoId)) {
        favorites = favorites.filter(id => id !== dinoId);
        button.classList.remove('active');
        showToast('❌ Eliminado de favoritos');
    } else {
        favorites.push(dinoId);
        button.classList.add('active');
        showToast('❤️ Agregado a favoritos');
    }
    
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #2D4A22;
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        z-index: 1000;
        font-size: 0.9rem;
        animation: fadeInOut 2s ease-in-out;
        pointer-events: none;
    `;
    
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// ============================================
// FILTRADO
// ============================================

async function filtrarPorDieta(dieta) {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        if (btn.dataset.filter === dieta) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    const grid = document.getElementById('dinosaursGrid');
    if (!grid) return;
    
    if (dieta === 'all') {
        cargarDinosaurios();
        return;
    }
    
    grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-dragon fa-spin"></i><p>Filtrando dinosaurios...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/dinosaurs/`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            const filtrados = data.data.filter(d => d.dieta && d.dieta.toLowerCase() === dieta.toLowerCase());
            
            if (filtrados.length > 0) {
                renderDinosaurios(filtrados);
                const resultsCount = document.getElementById('resultsCount');
                if (resultsCount) {
                    resultsCount.textContent = `${filtrados.length} dinosaurio(s) ${dieta}s`;
                }
            } else {
                grid.innerHTML = `
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <h3>No hay dinosaurios ${dieta}s</h3>
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error('Error filtrando:', error);
    }
}

// ============================================
// UTILIDADES
// ============================================

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderLocationSummary(ubicaciones) {
    if (!ubicaciones || ubicaciones.length === 0) {
        return '';
    }

    const visibles = ubicaciones.slice(0, 3).map((ubicacion) =>
        `<span class="location-chip"><i class="fas fa-location-dot"></i> ${escapeHtml(ubicacion.pais)}</span>`
    ).join('');

    return `
        <div class="location-summary">
            <strong>Dónde estuvo</strong>
            <div class="location-chips">${visibles}</div>
        </div>
    `;
}
