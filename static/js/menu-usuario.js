// ============================================
// MENÚ DE USUARIO (DROPDOWN)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const userMenuTrigger = document.getElementById('userMenuTrigger');
    const userDropdown = document.getElementById('userDropdown');
    
    // Contenido del dropdown (puedes personalizarlo)
    userDropdown.innerHTML = `
        <a href="/perfil"><i class="fas fa-user"></i> Mi perfil</a>
        <a href="/configuracion"><i class="fas fa-cog"></i> Configuración</a>
        <hr>
        <a href="/login"><i class="fas fa-sign-out-alt"></i> Cerrar sesión</a>
    `;
    
    // Toggle dropdown al hacer clic
    userMenuTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
    });
    
    // Cerrar dropdown al hacer clic fuera
    document.addEventListener('click', function() {
        userDropdown.classList.remove('show');
    });
    
    // Evitar que el clic dentro del dropdown lo cierre
    userDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});