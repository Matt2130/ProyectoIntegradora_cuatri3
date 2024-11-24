document.addEventListener('DOMContentLoaded', function() {
    //console.log(12345);
    fetch('/api/tabla_contact')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('administracion-tabla').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));

});

function eliminarProducto(param) {
    // Mostrar alerta de confirmación
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará los contactos. No podrás recuperarlos.",
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
            popup: 'mi-alerta-redondeada'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar pantalla de carga
            document.getElementById('loading').style.display = 'flex';
        
            // Enviar solicitud de eliminación
            fetch('/eliminar_contacto', {
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
                // Ocultar pantalla de carga y mostrar alerta de éxito
                document.getElementById('loading').style.display = 'none';
                Swal.fire({
                    title: 'Eliminado',
                    text: 'Contacto eliminado correctamente',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    background: '#bfbfbf',
                    showConfirmButton: false,
                    backdrop: 'rgba(0,0,0,0.7)',
                    timer: 4000,
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    window.location.href = '/administrador_contact';
                })

                setTimeout(() => {
                    window.open('/administrador_contact', '_self');
                }, 500);
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Error al eliminar el contacto',
                    textColor: '#fed800',
                    icon: 'error',
                    iconColor: '#ec221f',
                    background: '#bfbfbf',
                    backdrop: 'rgba(0,0,0,0.7)',
                    showConfirmButton: true,
                });
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
            });
        }
    });
}

//Modal registrar
function abrirModal() {
    var modal = document.getElementById("miModal");
    modal.style.display = "block"; // Muestra el modal

    var span = modal.getElementsByClassName("cerrar")[0];
    span.onclick = function() {
        modal.style.display = "none"; // Cierra el modal al hacer clic en la "X"
    }
    /*
    // Cierra el modal si se hace clic fuera de él
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
     */
}
////////////////////////////////////////////////////////////////////////////////

function registrarcontactos() {
    const facebook = document.getElementById('Facebook').value;
    const instagram = document.getElementById('Instagram').value;
    const tik_tok = document.getElementById('Tik_Tok').value;
    const email = document.getElementById('Email').value;
    const twitter = document.getElementById('Twiter').value;
    const whatsapp = document.getElementById('Whatsapp').value;
    const phone = document.getElementById('Telefono').value;

    // Validar que al menos un campo esté lleno
    if (!facebook && !instagram && !tik_tok && !email && !twitter && !whatsapp && !phone) {
        Swal.fire({
            title: 'Advertencia',
            text: 'Por favor, llena al menos un campo.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            backdrop: 'rgba(0,0,0,0.7)',
            timer: 4000,
            showConfirmButton: false,
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return;
    }

    document.getElementById('loading').style.display = 'flex';

    fetch('/registrar_contactos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok: tik_tok,
            email: email,
            twitter: twitter,
            whatsapp: whatsapp,
            phone: phone,
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                title: 'Éxito',
                text: 'Contacto registrado correctamente.',
                icon: 'success',
                iconColor: '#2b8c4b',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                timer: 4000,
                showConfirmButton: false,
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            });
            ActualizarProducto(); // Llama a la función necesaria para actualizar el producto
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Error',
                text: `Error al registrar: ${error.message}`,
                icon: 'error',
                iconColor: '#ec221f',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                timer: 4000,
                showConfirmButton: false,
                customClass: {
                    popup: 'mi-alerta-redondeada'
                }
            });
            document.getElementById('loading').style.display = 'none';
        });
}

//Modal edicion
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_contacto_edit', {
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

//Actualizar bd
function actualizartabalcontactos(idw) {
    const facebook = document.getElementById('Facebookd').value.trim();
    const instagram = document.getElementById('Instagramd').value.trim();
    const tik_tok = document.getElementById('Tik_Tokd').value.trim();
    const email = document.getElementById('Emaild').value.trim();
    const twitter = document.getElementById('Twiterd').value.trim();
    const whatsapp = document.getElementById('Whatsappd').value.trim();
    const phone = document.getElementById('Telefonod').value.trim();
    const id = idw;

    // Validar que al menos un campo esté lleno
    if (!facebook && !instagram && !tik_tok && !email && !twitter && !whatsapp && !phone) {
        Swal.fire({
            title: 'Advertencia',
            text: 'Por favor, llena al menos un campo.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            backdrop: 'rgba(0,0,0,0.7)',
            timer: 4000,
            showConfirmButton: false,
            customClass: {
                popup: 'mi-alerta-redondeada',
            },
        });
        return;
    }

    document.getElementById('loading').style.display = 'flex';

    fetch('/actualizar_contacto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok: tik_tok,
            email: email,
            twitter: twitter,
            whatsapp: whatsapp,
            phone: phone,
            id_contact: id,
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                title: 'Éxito',
                text: 'Contacto actualizado correctamente.',
                icon: 'success',
                iconColor: '#2b8c4b',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                timer: 4000,
                showConfirmButton: false,
                customClass: {
                    popup: 'mi-alerta-redondeada',
                },
            });
            ActualizarProducto();
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Error',
                text: `Error al actualizar el contacto: ${error.message}`,
                icon: 'error',
                iconColor: '#ec221f',
                confirmButtonColor: '#fed800',
                background: '#bfbfbf',
                backdrop: 'rgba(0,0,0,0.7)',
                timer: 4000,
                showConfirmButton: false,
                customClass: {
                    popup: 'mi-alerta-redondeada',
                },
            });
            document.getElementById('loading').style.display = 'none';
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
        window.location.href = '/administrador_contact';
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

function RegistrarProducto() {
    Swal.fire({
        title: 'Registro Exitoso',
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
        window.location.href = '/administrador_content';
    })
}