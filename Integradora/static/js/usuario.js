function eliminarusuariosolito(param) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el usuario. ¡No podrás recuperarlo!",
        icon: 'warning',
        iconColor: '#ec221f',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#fed800',
        confirmButtonText: 'Eliminar',
        background: '#bfbfbf',
        backdrop: 'rgba(0,0,0,0.7)',
        customClass: {
            popup: 'mi-alerta-redondeada' // Clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar la pantalla de carga
            document.getElementById('loading').style.display = 'flex';
        
            // Enviar solo el parámetro 'param' a Flask
            fetch('/eliminar_usuario_el_solito', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ parametro: param })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(() => {
                // Ocultar la pantalla de carga y mostrar alerta de éxito
                document.getElementById('loading').style.display = 'none';
                Swal.fire({
                    title: 'Eliminado',
                    text: 'El usuario se ha eliminado correctamente.',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    confirmButtonColor: '#fed800',
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    timer: 4000, // La alerta de éxito se cerrará automáticamente
                    showConfirmButton: false,
                    customClass: {
                        popup: 'mi-alerta-redondeada' // Clase personalizada
                    }
                }).then(() => {
                    window.open('/', '_self'); // Redirigir tras la eliminación
                });
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error',
                    text: "Error al eliminar: " + error.message,
                    icon: 'error',
                    iconColor: '#d33',
                    confirmButtonColor: '#fed800',
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    customClass: {
                        popup: 'mi-alerta-redondeada' // Clase personalizada
                    }
                });
            })
            .finally(() => {
                // Asegurarse de ocultar la pantalla de carga en cualquier caso
                document.getElementById('loading').style.display = 'none';
            });
        }
    });
}

//Modal para editar
function editarusuario() {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_users_edit_solo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({  })
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
window.onclick = function(event) {
    var modal = document.getElementById("miModal2");
    if (event.target === modal) {
        cerrarModal();
    }
}
///////Edicion sql usuario solo////////////
function editarsqlcontenidousuariosolo() {
    const usuario = document.getElementById('usuariod').value;
    const email = document.getElementById('emaild').value;
    const nombre = document.getElementById('nombred').value;
    const apellidop = document.getElementById('apellidopaternod').value;
    const apellidom = document.getElementById('apellidomaternod').value;
    const contraseñanueva = document.getElementById('contraseñanuevad').value;
    const contraseñaanterior = document.getElementById('contraseñaanteriord').value;

    if (!usuario || !email || !nombre || !apellidop || !apellidom || !contraseñaanterior) {
        Swal.fire({
            title: 'Error',
            text: 'Por favor, completa todos los campos excepto "Nueva contraseña" si no deseas cambiar la contraseña.',
            icon: 'warning',
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

    if (contraseñanueva) {
        const passwordPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (!passwordPattern.test(contraseñanueva)) {
            Swal.fire({
                title: 'Error',
                text: 'La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.',
                icon: 'warning',
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
    }

    const formData = new FormData();
    formData.append('usuario', usuario);
    formData.append('email', email);
    formData.append('nombre', nombre);
    formData.append('apellidop', apellidop);
    formData.append('apellidom', apellidom);
    formData.append('contraseñanueva', contraseñanueva);
    formData.append('contraseñaanterior', contraseñaanterior);

    // Expresión regular para validar correos
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Obtener el email del FormData
    const emailValue = formData.get('email');

    // Validar si el email tiene el formato correcto
    if (!emailPattern.test(emailValue)) {
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


    document.getElementById('loading').style.display = 'flex';

    fetch('/actualizar_usuario_solito', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        const status = response.status; // Guardamos el estado HTTP
        return response.json().then(data => ({ status, data }));
    })
    .then(({ status, data }) => {
        document.getElementById('loading').style.display = 'none';

        if (status === 200) {
            Swal.fire({
                title: 'Actualización exitosa',
                icon: 'success',
                iconColor: '#2b8c4b',
                showConfirmButton: false,
                timer: 3000,
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            }).then(() => {
                window.location.reload();
            });
        } else if (status === 400) {
            Swal.fire({
                title: 'Error',
                text: data.message, // Mensaje del backend
                icon: 'warning',
                iconColor: '#ec221f',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            });
        } else {
            Swal.fire({
                title: 'Error del servidor',
                text: 'Ocurrió un problema. Inténtalo más tarde.',
                icon: 'error',
                iconColor: '#ec221f',
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
        Swal.fire({
            title: 'Error',
            text: 'Error: ' + error.message,
            icon: 'error',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            backdrop: 'rgba(0,0,0,0.7)',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
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
function contraseña_incorrecta() {
    Swal.fire({
        icon: 'error',
        iconColor: '#ec221f',
        title: 'Error en el servidor',
        text: 'Contraseña incorrecta',
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

function ActualizarProducto() {
    Swal.fire({
        title: 'Actualización Exitosa',
        icon: 'success',
        iconColor: '#2b8c4b',
        showConfirmButton: false,
        timer: 2000,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'  // Clase personalizada
        }
    }).then(() => {
        window.location.reload();
    });
}