//console.log(1);
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
                alert(`Ningun campo puede estar vacio`);
                return;  // Detener la ejecución si algún campo está vacío
            }
        }
        // Expresión regular para validar la contraseña (sin necesidad de un carácter especial)
        const passwordPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

        // Verifica si la contraseña cumple con los criterios de seguridad
        if (!passwordPattern.test(formData.password)) {
            alert("La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.");
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
                // Si la respuesta no es exitosa (por ejemplo, 400 o 500), lanzar un error
                return response.json().then(data => {
                    throw new Error(data.message); // Lanzamos el mensaje de error desde la respuesta
                });
            }
            return response.json(); // Si todo va bien, seguimos con el procesamiento de la respuesta
        })
        .then(data => {
            console.log(data.message);
            document.getElementById('loading').style.display = 'none';
            alert("Registro exitoso: " + data.message);
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al registrar: " + error.message); // Mostrar alerta con el mensaje de error
        })
        .finally(() => {
            // Desaparecer la pantalla de carga
            document.getElementById('loading').style.display = 'none';
        });
    });
    
    /*
    document.getElementById('signupForm').addEventListener('submit', function(e) {
        
        e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        //Pantalla de carga
        document.getElementById('loading').style.display = 'flex';

        const formData = {
            name: document.getElementById('name').value,
            lastname: document.getElementById('lastname').value,
            surname: document.getElementById('surname').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };

        fetch('/registro_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            document.getElementById('loading').style.display = 'none';
            alert("Registro exitoso: " + data.message);
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al registrar: " + error.message); // Mostrar alerta de error
        })
        .finally(() => {
            // Desaparecer la pantalla de carga
            document.getElementById('loading').style.display = 'none';
        });
    });
     */
    //Iniciar secion
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();

        document.getElementById('loading').style.display = 'flex';

        // Obtener los datos del formulario
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
                // Redirigir a la URL proporcionada
                showAdminAccessAlert();
                setTimeout(() => {
                    window.open(data.redirect, '_self');
                }, 4000);
            }else{
                showInvalidCredentialsAlert();
            }
            
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading').style.display = 'none';
            showServerErrorAlert();
            //alert("Error al iniciar sesión: " + error.message);
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
        text: 'Accediendo como Administrador',
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