document.addEventListener('DOMContentLoaded', function() {
    cargarUsuarios(1); // Cargar la primera página de la tabla
});

// Función para cargar usuarios de una página específica
function cargarUsuarios(page) {
    fetch('/api/tabla_users?page=' + page)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            // Actualizar el contenido de la tabla
            document.getElementById('administracion-tabla').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}
function buscarUsuarios(buscar, page) {
    fetch('/api/buscador_users?page=' + page, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ buscar: buscar })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text();
    })
    .then(html => {
        // Actualiza la tabla con los resultados de búsqueda
        const resultsContainer = document.getElementById('administracion-tabla');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function PantallaeliminacionProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_users_delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text(); // Cambiado a text() para manejar HTML
    })
    .then(html => {
        // Inserta el HTML en el modal
        document.getElementById('miModal2').querySelector('.modal-contenido').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('miModal2').querySelector('.modal-contenido').innerText = 'Error en la edición';
    });
}

function eliminarProducto(param) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta operación no será reversible. ¿Deseas continuar?',
        icon: 'warning',
        iconColor: '#ec221f',
        showCancelButton: true,
        confirmButtonColor: '#fed800',
        cancelButtonColor: '#ec221f',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        background: '#bfbfbf', // Fondo gris
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const nuevo_user = document.getElementById('administradorEli').value;
            document.getElementById('loading').style.display = 'flex';

            // Enviar solicitud de eliminación
            fetch('/eliminar_usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ parametro: param, nuevo_user: nuevo_user })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(() => {
                document.getElementById('loading').style.display = 'none';
                Swal.fire({
                    title: 'Eliminación exitosa',
                    text: 'El usuario se ha eliminado correctamente.',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    showConfirmButton: false,
                    timer: 4000,
                    background: '#bfbfbf', // Fondo gris
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    window.open('/administrador_user', '_self'); // Redirigir tras éxito
                });
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loading').style.display = 'none';
                Swal.fire({
                    title: 'Error',
                    text: `Ocurrió un error al eliminar: ${error.message}`,
                    icon: 'error',
                    iconColor: '#ec221f',
                    showConfirmButton: false,
                    timer: 4000,
                    background: '#bfbfbf', // Fondo gris
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                });
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
            });
        }
    });
}

/////////////////////////////////////////////////
///Buscador
function buscador() {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ buscar: buscar })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text();
    })
    .then(html => {
        // Muestra los resultados HTML en el contenedor
        const resultsContainer = document.getElementById('administracion-tabla');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
//Modal para el registro
document.addEventListener("DOMContentLoaded", function() {
    // Obtiene el modal
    var modal = document.getElementById("miModal");

    // Obtiene el botón que abre la modal
    var btn = document.getElementById("abrirModal");

    // Obtiene el elemento <span> que cierra la modal
    var span = document.getElementsByClassName("cerrar")[0];

    // Cuando el usuario hace clic en el botón, se abre la modal
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // Cuando el usuario hace clic en <span> (x), se cierra la modal
    span.onclick = function() {
        modal.style.display = "none";
    }

});
//Modal para edición
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_users_edit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text(); // Cambiado a text() para manejar HTML
    })
    .then(html => {
        // Inserta el HTML en el modal
        document.getElementById('miModal2').querySelector('.modal-contenido').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('miModal2').querySelector('.modal-contenido').innerText = 'Error en la edición';
    });
}

function cerrarModal() {
    var modal = document.getElementById("miModal2");
    modal.style.display = "none";
}
/*
window.onclick = function(event) {
    var modal = document.getElementById("miModal2");
    if (event.target === modal) {
        cerrarModal();
    }
}
 */

//Modal para detalles
function detallesProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_users_detalles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text(); // Cambiado a text() para manejar HTML
    })
    .then(html => {
        // Inserta el HTML en el modal
        document.getElementById('miModal2').querySelector('.modal-contenido').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('miModal2').querySelector('.modal-contenido').innerText = 'Error en la edición';
    });
}
//Actualizacion
function editarsqlcontenido(idw) {
    const rol = document.getElementById('rol').value;
    const estado = document.getElementById('estado').value;
    const id = idw;

    if (!rol || !estado || !id) {
        Swal.fire({
            title: 'Advertencia',
            text: 'Por favor, completa todos los campos.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return; // Detener la ejecución si algún campo está vacío
    }

    document.getElementById('loading').style.display = 'flex';

    fetch('/actualizar_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rol: rol,
            estado: estado,
            id: id
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Actualización exitosa',
            text: data.message,
            icon: 'success',
            iconColor: '#2b8c4b',
            showConfirmButton: false,
            timer: 4000,
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        }).then(() => {
            window.location.href = '/administrador_user';
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Error',
            text: `Error al actualizar: ${error.message}`,
            icon: 'error',
            iconColor: '#ec221f',
            showConfirmButton: false,
            timer: 4000,
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
    });
}


//Registrar
function registrartemporadao() {
    const formData = {
        name: document.getElementById('name').value,
        lastname: document.getElementById('lastname').value,
        surname: document.getElementById('surname').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };

    if (!formData.name || !formData.lastname || !formData.surname || !formData.username || !formData.email || !formData.password) {
        // Mostrar alerta si hay campos vacíos
        Swal.fire({
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos antes de continuar.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada' // Clase personalizada (opcional)
            }
        });
        return; // Detener la ejecución si algún campo está vacío
    }

    // Expresión regular para validar correos
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Validar si el email tiene el formato correcto
    if (!emailPattern.test(formData.email)) {
        Swal.fire({
            title: 'Error',
            text: 'El correo electrónico ingresado no es válido. Por favor, verifica.',
            icon: 'error',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            backdrop: 'rgba(0,0,0,0.7)',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return;
    } 

    // Mostrar pantalla de carga
    document.getElementById('loading').style.display = 'flex';

    fetch('/registro_usuario_administrador', {
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
        Swal.fire({
            title: 'Registro exitoso',
            text: 'Usuario registrado correctamente.',
            icon: 'success',
            iconColor: '#2b8c4b',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada' // Clase personalizada (opcional)
            }
        }).then(() => {
            window.location.reload(); // Recargar la página tras cerrar la alerta
        });
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            title: 'Error',
            text: "Error al registrar: " + error.message,
            icon: 'error',
            iconColor: '#d33',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada' // Clase personalizada (opcional)
            }
        });
    })
    .finally(() => {
        // Desaparecer la pantalla de carga
        document.getElementById('loading').style.display = 'none';
    });
}
