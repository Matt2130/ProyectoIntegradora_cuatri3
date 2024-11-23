// console.log(1);
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('signupForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        const formData = {
            name: document.getElementById('name').value,
            lastname: document.getElementById('lastname').value,
            surname: document.getElementById('surname').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };
        
        for (const key in formData) {
            if (!formData[key]) {  // Si algún campo está vacío
                Swal.fire({
                    title: 'Error',
                    text: 'Ningún campo puede estar vacío.',
                    icon: 'warning',
                    iconColor: '#000000',
                    confirmButtonColor: '#fed800',
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                });
                return;  // Detener la ejecución si algún campo está vacío
            }
        }
        // Expresión regular para validar la contraseña (sin necesidad de un carácter especial)
        const passwordPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

        // Verifica si la contraseña cumple con los criterios de seguridad
        if (!passwordPattern.test(formData.password)) {
            Swal.fire({
                title: 'Error',
                text: 'La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.',
                icon: 'warning',
                iconColor: '#000000',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            });
            return;  // Detener la ejecución si la contraseña no cumple con los requisitos
        }

        // Pantalla de carga
        document.getElementById('loading').style.display = 'flex';

        fetch('/registro_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            document.getElementById('loading').style.display = 'none';
            Swal.fire({
                title: 'Registro exitoso',
                text: data.message,
                icon: 'success',
                iconColor: '#2b8c4b',
                showConfirmButton: false, // No muestra botón
                timer: 3000, // Desaparece automáticamente
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            }).then(() => {
                window.location.reload();
            });
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Error',
                text: 'Error al registrar: ' + error.message,
                icon: 'error',
                iconColor: '#d33',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            });
        })
        .finally(() => {
            document.getElementById('loading').style.display = 'none';
        });
    });

    // Iniciar sesión
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();

        document.getElementById('loading').style.display = 'flex';

        const formData = {
            email: document.getElementById('email2').value,
            password: document.getElementById('password2').value,
        };

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                showServerErrorAlert();
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            if (data.redirect) {
                Swal.fire({
                    title: 'Acceso concedido',
                    text: 'Bienvenido administrador. Redirigiendo...',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    showConfirmButton: false, // No muestra botón
                    timer: 3000, // Desaparece automáticamente
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    window.open(data.redirect, '_self');
                });
            } else {
                Swal.fire({
                    title: 'Credenciales inválidas',
                    text: 'El correo o la contraseña no son correctos.',
                    icon: 'error',
                    iconColor: '#d33',
                    confirmButtonColor: '#fed800',
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading').style.display = 'none';
            showServerErrorAlert();
        });
    });
});

////Alertas Manuel
// Alerta para acceso como Cliente
function showClientAccessAlert() {
    Swal.fire({
        icon: 'success',
        iconColor: '#2b8c4b',
        title: '¡Bienvenido!',
        text: 'Accediendo como Cliente',
        timer: 2000,
        showConfirmButton: false,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then(() => {
        window.location.href = "/cliente";
    });
}
function showAdminAccessAlert() {
    Swal.fire({
        icon: 'success',
        iconColor: '#2b8c4b',
        title: '¡Bienvenido!',
        text: 'Accediendo',
        timer: 2000,
        showConfirmButton: false,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then(() => {
        window.location.href = "/administrador_productos";
    });
}
// Alerta de error en el servidor
function showServerErrorAlert() {
    Swal.fire({
        icon: 'error',
        iconColor: '#ec221f',
        title: 'Error en el servidor',
        text: 'Hubo un problema al procesar tu solicitud. Intenta nuevamente más tarde',
        showConfirmButton: false,
        showCancelButton: true,
        cancelButtonColor: '#fed800',
        cancelButtonText: 'OK',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    });
}
// Alerta de usuario o contraseña incorrectos
function showInvalidCredentialsAlert() {
    Swal.fire({
        icon: 'error',
        iconColor: '#ec221f',
        showConfirmButton: false,
        showCancelButton: true,
        cancelButtonColor: '#fed800',
        cancelButtonText: 'OK',
        title: 'Error',
        text: 'Usuario o contraseña incorrectos',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    });
}