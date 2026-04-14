// ============================================
// DINOSAURIOS FLOTANTES DE FONDO
// ============================================
function createDinoBackground() {
    const container = document.getElementById('dino-bg-container');
    if (!container) return;
    
    const dinoImages = [
        '../static/img/dinosauriof1.png',
        '../static/img/dinosauriof2.png',
        '../static/img/dinosauriof3.png',
        '../static/img/dinosauriof4.png',
        '../static/img/dinosauriof5.png',
        '../static/img/dinosauriof6.png',
        '../static/img/dinosauriof7.png',
        '../static/img/dinosauriof8.png',
        '../static/img/dinosauriof9.png'
    ];
    
    for (let i = 0; i < 18; i++) {
        const dinoDiv = document.createElement('div');
        dinoDiv.className = 'dino-bg';
        
        const img = document.createElement('img');
        const randomIndex = Math.floor(Math.random() * dinoImages.length);
        img.src = dinoImages[randomIndex];
        img.alt = 'Dinosaurio fondo';
        
        dinoDiv.appendChild(img);
        
        dinoDiv.style.left = Math.random() * 100 + '%';
        const duration = 15 + Math.random() * 20;
        dinoDiv.style.animationDuration = duration + 's';
        dinoDiv.style.animationDelay = Math.random() * 15 + 's';
        const size = 40 + Math.random() * 60;
        dinoDiv.style.width = size + 'px';
        
        container.appendChild(dinoDiv);
    }
}

// ============================================
// USUARIOS DE DEMOSTRACIÓN (simulando base de datos)
// ============================================
const demoUsers = [
    { username: "Anchornis", email: "anchornis@dino.com", password: "Dino123!" },
    { username: "Zaid", email: "zaid@dino.com", password: "Dino123!" },
    { username: "demo", email: "demo@dino.com", password: "Dino123!" }
];

// ============================================
// VALIDAR CREDENCIALES
// ============================================
function validateCredentials(identifier, password) {
    // Buscar por username o email
    return demoUsers.find(user => 
        (user.username === identifier || user.email === identifier) && 
        user.password === password
    );
}

// ============================================
// MOSTRAR MENSAJE DE ERROR
// ============================================
function showError(message) {
    // Crear elemento de error si no existe
    let errorDiv = document.getElementById('loginError');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'loginError';
        errorDiv.style.cssText = `
            background: #E74C3C;
            color: white;
            padding: 12px;
            border-radius: 60px;
            text-align: center;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            animation: slideUp 0.5s ease;
        `;
        const form = document.getElementById('loginForm');
        form.appendChild(errorDiv);
    }
    
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    errorDiv.style.display = 'flex';
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}

// ============================================
// INICIALIZAR EVENTOS
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Crear dinosaurios flotantes
    createDinoBackground();
    
    const form = document.getElementById('loginForm');
    const successDiv = document.getElementById('successMessage');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    // Submit del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const identifier = usernameInput.value.trim();
        const password = passwordInput.value;
        
        // Validar campos vacíos
        if (identifier === '') {
            showError("❌ Ingresa tu nombre de usuario o email");
            usernameInput.focus();
            return;
        }
        
        if (password === '') {
            showError("❌ Ingresa tu contraseña");
            passwordInput.focus();
            return;
        }
        
        // Validar credenciales
        const user = validateCredentials(identifier, password);
        
        if (!user) {
            showError("❌ Usuario o contraseña incorrectos. ¿Probaste con demo@dino.com / Dino123!?");
            passwordInput.value = '';
            passwordInput.focus();
            return;
        }
        
        // ============================================
        // INICIO DE SESIÓN EXITOSO
        // ============================================
        
        // Guardar usuario en localStorage
        localStorage.setItem('currentUser', JSON.stringify({
            username: user.username,
            email: user.email
        }));
        
        // Mostrar mensaje de éxito
        successDiv.classList.add('show');
        
        // Animación de "romper huevo"
        const container = document.querySelector('.login-container');
        container.style.transform = 'scale(0.98)';
        setTimeout(() => {
            container.style.transform = '';
        }, 200);
        
        // Redirigir después de 2 segundos
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
    });
    
    // Limpiar mensaje de error al escribir
    usernameInput.addEventListener('input', () => {
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) errorDiv.style.display = 'none';
    });
    
    passwordInput.addEventListener('input', () => {
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) errorDiv.style.display = 'none';
    });
});