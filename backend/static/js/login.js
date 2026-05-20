// ============================================
// DINOSAURIOS FLOTANTES DE FONDO
// ============================================
function createDinoBackground() {
    const container = document.getElementById('dino-bg-container');
    if (!container) return;
    
    const dinoImages = [
        '/static/img/dinosauriof1.png',
        '/static/img/dinosauriof2.png',
        '/static/img/dinosauriof3.png',
        '/static/img/dinosauriof4.png',
        '/static/img/dinosauriof5.png',
        '/static/img/dinosauriof6.png',
        '/static/img/dinosauriof7.png',
        '/static/img/dinosauriof8.png',
        '/static/img/dinosauriof9.png'
    ];
    
    for (let i = 0; i < 18; i++) {
        const dinoDiv = document.createElement('div');
        dinoDiv.className = 'dino-bg';
        
        const img = document.createElement('img');
        const randomIndex = Math.floor(Math.random() * dinoImages.length);
        img.src = dinoImages[randomIndex];
        img.alt = 'Dinosaurio fondo';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'contain';
        
        dinoDiv.appendChild(img);
        
        dinoDiv.style.left = Math.random() * 100 + '%';
        const duration = 15 + Math.random() * 20;
        dinoDiv.style.animationDuration = duration + 's';
        dinoDiv.style.animationDelay = Math.random() * 15 + 's';
        const size = 40 + Math.random() * 60;
        dinoDiv.style.width = size + 'px';
        dinoDiv.style.height = 'auto';
        
        container.appendChild(dinoDiv);
    }
}

function showError(message) {
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
        `;
        const form = document.getElementById('loginForm');
        if (form) form.appendChild(errorDiv);
    }
    
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i><span>${message}</span>`;
    errorDiv.style.display = 'flex';
    
    setTimeout(() => {
        if (errorDiv) errorDiv.style.display = 'none';
    }, 3000);
}

function mostrarExito(mensaje) {
    const successDiv = document.getElementById('successMessage');
    if (successDiv) {
        successDiv.innerHTML = `
            <img src="/static/img/huella.png" alt="Huella" class="success-icon">
            <span>${mensaje}</span>
        `;
        successDiv.classList.add('show');
        successDiv.style.display = 'block';
        
        const container = document.querySelector('.login-container');
        if (container) {
            container.style.transform = 'scale(0.98)';
            setTimeout(() => {
                container.style.transform = '';
            }, 200);
        }
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    createDinoBackground();
    
    const form = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (!form) {
        console.error('Formulario de login no encontrado');
        return;
    }
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const identifier = usernameInput.value.trim();
        const password = passwordInput.value;
        
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
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.innerHTML : 'Iniciar Sesión';
        if (submitBtn) {
            submitBtn.innerHTML = '<span>⏳ Validando...</span>';
            submitBtn.disabled = true;
        }
        
        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: identifier, password: password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('currentUser', JSON.stringify({
                    id: data.id,
                    nombre: data.nombre,
                    username: data.username,
                    email: data.email
                }));
                
                mostrarExito("✅ ¡Inicio de sesión exitoso! Redirigiendo...");
                
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                showError(data.detail || "❌ Usuario o contraseña incorrectos");
                passwordInput.value = '';
                passwordInput.focus();
                if (submitBtn) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showError("❌ Error de conexión con el servidor");
            if (submitBtn) {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        }
    });
    
    usernameInput.addEventListener('input', () => {
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) errorDiv.style.display = 'none';
    });
    
    passwordInput.addEventListener('input', () => {
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) errorDiv.style.display = 'none';
    });
});