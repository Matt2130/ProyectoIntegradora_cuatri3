document.addEventListener('DOMContentLoaded', function() {
    // Obtener los parámetros de la URL actual
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id');
    //console.log('Valor de id:', id);

    fetch('/api/comentarios_producto', {
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
        return response.text();
    })
    .then(html => {
        // Muestra los resultados HTML en el contenedor
        const resultsContainer = document.getElementById('comentario_del_producto');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function registrarcomentario() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id');
    let comentario = document.getElementById('nuevo-comentario').value.trim();
    let calif = document.getElementById('califa').value;

    // Validación de campos
    if (!calif) {
        Swal.fire({
            title: 'Advertencia',
            text: 'Por favor, llena el campo de calificación.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return;
    }

    document.getElementById('loading').style.display = 'flex';

    fetch('/registrar_comentario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: id,
            calificacion: calif,
            comentario: comentario,
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message); });
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Registro exitoso',
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
            window.location.reload(); // Recarga solo la sección de comentarios
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Error',
            text: `Error al registrar el comentario: ${error.message}`,
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

//Eliminar comentario

function eliminarComentario(param) {
    // Mostrar alerta de confirmación
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el comentario. No podrás recuperarlos.",
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
            fetch('/eliminar_comentario_producto', {
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
                    text: 'Comentario eliminado correctamente',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    background: '#bfbfbf',
                    showConfirmButton: false,
                    backdrop: 'rgba(0,0,0,0.7)',
                    timer: 2000,
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    window.location.reload();
                })
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

////Edicion de comentario modal
//Modal para edición
function editarComentario(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_comentario_edit', {
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
//////////////////////////////////////////////////////////////////////
function editarsqlcomentario(id_comentario) {
    const comentario = document.getElementById('comentariod').value;
    const calif = document.getElementById('califad').value;

    if (!calif) {
        Swal.fire({
            title: 'Advertencia',
            text: 'Por favor, llena el campo de calificación.',
            icon: 'warning',
            iconColor: '#ec221f',
            confirmButtonColor: '#fed800',
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return;
    }

    document.getElementById('loading').style.display = 'flex';

    fetch('/actualizar_comentario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            comentario: comentario,
            calif: calif,
            id_comentario: id_comentario,
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
            text: 'El comentario se ha actualizado correctamente.',
            icon: 'success',
            iconColor: '#2b8c4b',
            showConfirmButton: false,
            timer: 4000,
            background: '#bfbfbf',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        }).then(() => {
            ActualizarProducto(); // Llamar la función tras el éxito
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Error',
            text: `Ocurrió un error al actualizar: ${error.message}`,
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
    })
}