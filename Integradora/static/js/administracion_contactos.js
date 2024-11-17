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
        iconColor: '#000000',
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

    // Cierra el modal si se hace clic fuera de él
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}
////////////////////////////////////////////////////////////////////////////////

function registrarcontactos(){
    //console.log(3456789);
    
    const facebook = document.getElementById('Facebook').value;
    const instagram = document.getElementById('Instagram').value;
    const tik_tok = document.getElementById('Tik_Tok').value;
    const email = document.getElementById('Email').value;
    const twitter = document.getElementById('Twiter').value;
    const whatsapp = document.getElementById('Whatsapp').value;
    const phone = document.getElementById('Telefono').value;

    fetch('/registrar_contactos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok:tik_tok,
            email:email,
            twitter:twitter,
            whatsapp:whatsapp,
            phone:phone

        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        ActualizarProducto();
/*         alert(data.message); 
        window.location.href = '/administrador_contact'; */
    })
    .catch(error => {
        console.error('Error:', error);
/*         alert("Error al registrar: " + error.message); */
        showServerErrorAlert();
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
window.onclick = function(event) {
    var modal = document.getElementById("miModal2");
    if (event.target === modal) {
        cerrarModal();
    }
}

//Actualizar bd
function actualizartabalcontactos(idw){
    //console.log(idw);
    const facebook = document.getElementById('Facebookd').value;
    const instagram = document.getElementById('Instagramd').value;
    const tik_tok = document.getElementById('Tik_Tokd').value;
    const email = document.getElementById('Emaild').value;
    const twitter = document.getElementById('Twiterd').value;
    const whatsapp = document.getElementById('Whatsappd').value;
    const phone = document.getElementById('Telefonod').value;
    const id = idw;

    fetch('/actualizar_contacto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facebook: facebook,
            instagram: instagram,
            tik_tok:tik_tok,
            email:email,
            twitter:twitter,
            whatsapp:whatsapp,
            phone:phone,
            id_contact: id
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        ActualizarProducto();
        /* alert(data.message); */ 
        //window.location.href = '/administrador_contact';
    })
    .catch(error => {
        console.error('Error:', error);
/*         alert("Error al actualizar: " + error.message); */
        showServerErrorAlert();
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