document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tabla_content')
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
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el contenido. ¡No podrás recuperarlo!",
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
            // Mostrar la pantalla de carga
            document.getElementById('loading').style.display = 'flex';

            // Enviar solo el parámetro 'param' a Flask
            fetch('/eliminar_contenido', {
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
                    text: 'Contenido eliminado correctamente.',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    background: '#bfbfbf',
                    confirmButtonColor: '#fed800',
                    showConfirmButton: false,
                    backdrop: 'rgba(0,0,0,0.7)',
                    timer: 2000, // La alerta de éxito se cerrará automáticamente
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    // Redirigir después del éxito
                    window.location.href = '/administrador_content';
                });
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loading').style.display = 'none';
                Swal.fire({
                    title: 'Error',
                    text: "Error al eliminar: " + error.message,
                    icon: 'error',
                    background: '#bfbfbf',
                    confirmButtonColor: '#d33',
                    customClass: {
                        popup: 'mi-alerta-redondeada'
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

/////////////////////////////////////////////////////////////////////////////////////////
//Buscador
function buscador() {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_content', {
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
        return response.text();  // Cambiado de .json() a .text() para recibir HTML
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

///////////////////////////////////////////////////
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

    fetch('/api/buscador_content_edit', {
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
//Actualizacion
function editarsqlcontenido(contenidoId) {
    const titulo = document.getElementById('tituloedit').value.trim();
    const descripcion = document.getElementById('descripcionedit').value.trim();

    // Validar que los campos no estén vacíos
    if (!titulo || !descripcion) {
        Swal.fire({
            title: 'Advertencia',
            text: 'El título y la descripción no pueden estar vacíos.',
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

    // Confirmar la acción con SweetAlert2
    Swal.fire({
        title: '¿Estás seguro?',
        text: '¿Deseas actualizar este contenido?',
        icon: 'question',
        iconColor: '#ec221f',
        showCancelButton: true,
        confirmButtonText: 'Sí, actualizar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#fed800',
        cancelButtonColor: '#ec221f',
        background: '#bfbfbf',
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('loading').style.display = 'flex';

            // Enviar la solicitud para actualizar el contenido
            fetch('/actualizar_contenido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    titulo: titulo,
                    descripcion: descripcion,
                    id: contenidoId,
                }),
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(data => {
                            throw new Error(data.message || 'Error al actualizar contenido');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    Swal.fire({
                        title: 'Actualización exitosa',
                        text: data.message || 'El contenido ha sido actualizado correctamente.',
                        icon: 'success',
                        iconColor: '#2b8c4b',
                        showConfirmButton: false,
                        timer: 4000,
                        background: '#bfbfbf',
                        customClass: {
                            popup: 'mi-alerta-redondeada'
                        }
                    });
                    // Redireccionar si es necesario
                    // window.location.href = '/administrador_content';
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
    });
}

////////////////////////////////////////////////////////////////////////////////
function registrarcontenido() {
    const titulo = document.getElementById('titulo').value.trim();
    const descripcion = document.getElementById('descripcion').value.trim();

    if (!titulo || !descripcion) {
        Swal.fire({
            title: 'Advertencia',
            text: 'El título y la descripción no pueden estar vacíos.',
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

    fetch('/registrar_contenido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ titulo, descripcion }),
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Error al registrar contenido');
                });
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                title: 'Éxito',
                text: 'Contenido registrado correctamente.',
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
            RegistrarProducto(); // Llamada a la función de registro de productos
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
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
            console.error('Error:', error);
            document.getElementById('loading').style.display = 'none';
        });
}

//////////////Mostrar contenido de la base de datos//////////////////
//Todos se pueden a la vez
/*
function toggleExpand(event, element) {
    if (event.target.tagName !== 'BUTTON') { // Solo expande si no se ha hecho clic en un botón
      element.classList.toggle("expanded");
    }
}
 */
//Uno a la vez
function toggleExpand(event, element) {
    if (event.target.tagName !== 'BUTTON') { // Solo expande si no se ha hecho clic en un botón
        const allContents = document.querySelectorAll('.content');
        allContents.forEach(content => {
            if (content !== element) { // Cierra los demás contenidos
                content.classList.remove("expanded");
            }
        });
        element.classList.toggle("expanded"); // Alterna el estado del div clicado
    }
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
        window.location.href = '/administrador_content';
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