// ============================================
// DINOSAURIOS FLOTANTES DE FONDO (imágenes f1 a f9)
// ============================================
function createDinoBackground() {
    const container = document.getElementById('dino-bg-container');

    // Tus 9 imágenes de dinosaurios
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
// VALIDACIÓN DE CONTRASEÑA FUERTE
// ============================================
function checkPasswordStrength(password) {
    const requirements = {
        mayuscula: /[A-Z]/.test(password),
        minuscula: /[a-z]/.test(password),
        numero: /[0-9]/.test(password),
        especial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
        longitud: password.length >= 8
    };

    // Actualizar colores de la lista
    const reqMayuscula = document.getElementById('req-mayuscula');
    const reqMinuscula = document.getElementById('req-minuscula');
    const reqNumero = document.getElementById('req-numero');
    const reqEspecial = document.getElementById('req-especial');
    const reqLongitud = document.getElementById('req-longitud');

    // Función para actualizar cada requisito
    function updateRequirement(element, isValid) {
        if (isValid) {
            element.classList.add('valid');
            element.classList.remove('invalid', 'neutral');
            element.querySelector('i').className = 'fas fa-check-circle';
        } else if (password.length === 0) {
            element.classList.add('neutral');
            element.classList.remove('valid', 'invalid');
            element.querySelector('i').className = 'fas fa-circle';
        } else {
            element.classList.add('invalid');
            element.classList.remove('valid', 'neutral');
            element.querySelector('i').className = 'fas fa-times-circle';
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

// ============================================
// VALIDAR COINCIDENCIA DE CONTRASEÑAS
// ============================================
function checkPasswordsMatch(password, confirmPassword) {
    const matchMessage = document.getElementById('matchMessage');

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

// ============================================
// INICIALIZAR EVENTOS
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    createDinoBackground();

    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirmPassword');
    const form = document.getElementById('registroForm');
    const successDiv = document.getElementById('successMessage');

    // Inicializar requisitos en estado neutral
    const allReqs = document.querySelectorAll('.password-requirements li');
    allReqs.forEach(req => {
        req.classList.add('neutral');
        req.classList.remove('valid', 'invalid');
        req.querySelector('i').className = 'fas fa-circle';
    });

    // Evento para validar contraseña en tiempo real
    passwordInput.addEventListener('input', function () {
        const password = this.value;
        checkPasswordStrength(password);

        if (confirmInput.value !== '') {
            checkPasswordsMatch(password, confirmInput.value);
        }
    });

    // Evento para validar coincidencia en tiempo real
    confirmInput.addEventListener('input', function () {
        const password = passwordInput.value;
        const confirmPassword = this.value;
        checkPasswordsMatch(password, confirmPassword);
    });

    // Submit del formulario
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value.trim();
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmInput.value;

        // Validar nombre
        if (nombre.length < 2) {
            alert("❌ El nombre debe tener al menos 2 letras.");
            document.getElementById('nombre').focus();
            return;
        }

        if (username.length < 3) {
            alert("❌ El nombre de usuario debe tener al menos 3 caracteres.");
            document.getElementById('username').focus();
            return;
        }


        // Validar email
        if (!email.includes('@') || !email.includes('.')) {
            alert("❌ Correo electrónico no válido.");
            document.getElementById('email').focus();
            return;
        }

        // Validar contraseña fuerte
        const isPasswordStrong = checkPasswordStrength(password);
        if (!isPasswordStrong) {
            alert("❌ La contraseña no cumple con todos los requisitos.\n\nRequisitos:\n- 1 mayúscula\n- 1 minúscula\n- 1 número\n- 1 carácter especial\n- Mínimo 8 caracteres");
            passwordInput.focus();
            return;
        }

        // Validar que coincidan las contraseñas
        if (password !== confirmPassword) {
            alert("❌ Las contraseñas no coinciden.");
            confirmInput.focus();
            return;
        }

        // ============================================
        // SOLO AQUÍ SE MUESTRA EL MENSAJE DE ÉXITO
        // ============================================
        successDiv.classList.add('show');

        // Animación de "romper huevo"
        const container = document.querySelector('.register-container');
        container.style.transform = 'scale(0.98)';
        setTimeout(() => {
            container.style.transform = '';
        }, 200);

        // Ocultar mensaje y limpiar formulario después de 4 segundos
        setTimeout(() => {
            successDiv.classList.remove('show');
            form.reset();

            // Resetear validaciones visuales
            const allReqs = document.querySelectorAll('.password-requirements li');
            allReqs.forEach(req => {
                req.classList.add('neutral');
                req.classList.remove('valid', 'invalid');
                req.querySelector('i').className = 'fas fa-circle';
            });
            document.getElementById('matchMessage').innerHTML = '';
        }, 4000);
    });
});