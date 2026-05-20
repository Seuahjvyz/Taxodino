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

// ============================================
// VALIDACIÓN DE CONTRASEÑA
// ============================================
function checkPasswordStrength(password) {
    const requirements = {
        mayuscula: /[A-Z]/.test(password),
        minuscula: /[a-z]/.test(password),
        numero: /[0-9]/.test(password),
        especial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
        longitud: password.length >= 8
    };

    const reqMayuscula = document.getElementById('req-mayuscula');
    const reqMinuscula = document.getElementById('req-minuscula');
    const reqNumero = document.getElementById('req-numero');
    const reqEspecial = document.getElementById('req-especial');
    const reqLongitud = document.getElementById('req-longitud');

    function updateRequirement(element, isValid) {
        if (!element) return;
        if (isValid) {
            element.classList.add('valid');
            element.classList.remove('invalid', 'neutral');
            const icon = element.querySelector('i');
            if (icon) icon.className = 'fas fa-check-circle';
        } else if (password.length === 0) {
            element.classList.add('neutral');
            element.classList.remove('valid', 'invalid');
            const icon = element.querySelector('i');
            if (icon) icon.className = 'fas fa-circle';
        } else {
            element.classList.add('invalid');
            element.classList.remove('valid', 'neutral');
            const icon = element.querySelector('i');
            if (icon) icon.className = 'fas fa-times-circle';
        }
    }

    updateRequirement(reqMayuscula, requirements.mayuscula);
    updateRequirement(reqMinuscula, requirements.minuscula);
    updateRequirement(reqNumero, requirements.numero);
    updateRequirement(reqEspecial, requirements.especial);
    updateRequirement(reqLongitud, requirements.longitud);

    return requirements.mayuscula && requirements.minuscula &&
           requirements.numero && requirements.especial && requirements.longitud;
}

function checkPasswordsMatch(password, confirmPassword) {
    const matchMessage = document.getElementById('matchMessage');
    if (!matchMessage) return false;

    if (confirmPassword === '') {
        matchMessage.innerHTML = '';
        matchMessage.className = 'password-match-message';
        return false;
    }

    if (password === confirmPassword) {
        matchMessage.innerHTML = '<i class="fas fa-check-circle"></i> Las contraseñas coinciden';
        matchMessage.className = 'password-match-message match-success';
        return true;
    } else {
        matchMessage.innerHTML = '<i class="fas fa-times-circle"></i> Las contraseñas no coinciden';
        matchMessage.className = 'password-match-message match-error';
        return false;
    }
}

function mostrarError(mensaje) {
    const toast = document.createElement('div');
    toast.textContent = mensaje;
    toast.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#e74c3c;color:white;padding:12px 24px;border-radius:8px;z-index:1000;font-size:14px;animation:slideIn 0.3s ease;box-shadow:0 2px 10px rgba(0,0,0,0.2);max-width:350px;white-space:pre-line;';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function mostrarExito(mensaje) {
    const successDiv = document.getElementById('successMessage');
    if (successDiv) {
        successDiv.textContent = mensaje;
        successDiv.classList.add('show');
        successDiv.style.display = 'block';
        
        const container = document.querySelector('.register-container');
        if (container) {
            container.style.transform = 'scale(0.98)';
            setTimeout(() => {
                container.style.transform = '';
            }, 200);
        }
        
        setTimeout(() => {
            successDiv.classList.remove('show');
            successDiv.style.display = 'none';
            window.location.href = '/login';
        }, 2000);
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registroForm');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirmPassword');

    if (!form) {
        console.error('Formulario de registro no encontrado');
        return;
    }

    createDinoBackground();

    const allReqs = document.querySelectorAll('.password-requirements li');
    if (allReqs.length > 0) {
        allReqs.forEach(req => {
            req.classList.add('neutral');
            req.classList.remove('valid', 'invalid');
            const icon = req.querySelector('i');
            if (icon) icon.className = 'fas fa-circle';
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const password = this.value;
            checkPasswordStrength(password);
            if (confirmInput && confirmInput.value !== '') {
                checkPasswordsMatch(password, confirmInput.value);
            }
        });
    }

    if (confirmInput) {
        confirmInput.addEventListener('input', function () {
            if (passwordInput) {
                checkPasswordsMatch(passwordInput.value, this.value);
            }
        });
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        
        const nombre = document.getElementById('nombre')?.value.trim() || '';
        const username = document.getElementById('username')?.value.trim() || '';
        const email = document.getElementById('email')?.value.trim() || '';
        const password = passwordInput?.value || '';
        const confirmPassword = confirmInput?.value || '';

        if (nombre.length < 5) {
            mostrarError("El nombre debe tener al menos 2 letras.");
            document.getElementById('nombre')?.focus();
            return;
        }

        if (username.length < 3) {
            mostrarError("El nombre de usuario debe tener al menos 3 caracteres.");
            document.getElementById('username')?.focus();
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            mostrarError("Correo electrónico no válido.");
            document.getElementById('email')?.focus();
            return;
        }

        const isPasswordStrong = checkPasswordStrength(password);
        if (!isPasswordStrong) {
            mostrarError("La contraseña no cumple con los requisitos.");
            passwordInput?.focus();
            return;
        }

        if (password !== confirmPassword) {
            mostrarError("Las contraseñas no coinciden.");
            confirmInput?.focus();
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.textContent : 'Registrar';
        if (submitBtn) {
            submitBtn.textContent = 'Registrando...';
            submitBtn.disabled = true;
        }

        try {
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, username, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                mostrarExito("Registro exitoso! Redirigiendo al login...");
                form.reset();
            } else {
                mostrarError(data.detail || data.message || "Error en el registro");
                if (submitBtn) {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarError("Error de conexión con el servidor");
            if (submitBtn) {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        }
    });
});

if (!document.querySelector('#dino-animation-style')) {
    const style = document.createElement('style');
    style.id = 'dino-animation-style';
    style.textContent = '@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }';
    document.head.appendChild(style);
}
