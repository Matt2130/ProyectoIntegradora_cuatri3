document.addEventListener('DOMContentLoaded', function() {
    cargarProductos(1);  // Cargar la primera página de la tabla
});

// Función para cargar productos de una página específica
function cargarProductos(page) {
    fetch('/api/tabla_productos?page=' + page)
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

/*
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tabla_productos')
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
 */

function eliminarProducto(param) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el producto. ¡No podrás recuperarlo!",
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
            fetch('/eliminar_producto', {
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
                    text: 'Producto eliminado correctamente.',
                    icon: 'success',
                    iconColor: '#2b8c4b',
                    background: '#bfbfbf',
                    confirmButtonColor: '#fed800',
                    backdrop: 'rgba(0,0,0,0.7)',
                    timer: 4000, // La alerta de éxito se cerrará automáticamente
                    customClass: {
                        popup: 'mi-alerta-redondeada'
                    }
                }).then(() => {
                    // Redirigir después del éxito
                    window.open('/administrador_productos', '_self');
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
function buscador(page = 1) {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_productos?page=' + page, {
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
        return response.text();  // Recibe el HTML para actualizar la tabla
    })
    .then(html => {
        // Actualiza el contenido de la tabla
        const resultsContainer = document.getElementById('administracion-tabla');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

///Modal de registro
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

//Registrar
function registrarproducto() {
    // Obtén los datos
    const temporada = document.getElementById('temporada').value;
    const tamaño = document.getElementById('tamaño').value;
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;
    const precio_lot = document.getElementById('precio_lot').value;
    const color = document.getElementById('color').value;
    const materia = document.getElementById('materia').value;

    if (!temporada || !tamaño || !nombre || !descripcion || !precio_lot || !color) {
        Swal.fire({
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos. (Exceptuando Material)',
            icon: 'warning',
            iconColor: '#ec221f',
            showConfirmButton: false,
            timer: 4000,
            background: '#f8d7da',
            backdrop: 'rgba(0,0,0,0.7)',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        return; // Detener la ejecución si algún campo está vacío
    }

    // Crear un FormData
    const formData = new FormData();
    formData.append('image', image);
    formData.append('modelo', modelo);
    formData.append('temporada', temporada);
    formData.append('tamaño', tamaño);
    formData.append('nombre', nombre);
    formData.append('descripcion', descripcion);
    formData.append('precio_lot', precio_lot);
    formData.append('color', color);
    formData.append('materia', materia);

    document.getElementById('loading').style.display = 'flex';

    fetch('/registrar_producto', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        RegistrarProducto();
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Producto registrado',
            text: 'El producto se ha registrado correctamente.',
            icon: 'success',
            iconColor: '#2b8c4b',
            showConfirmButton: false,
            timer: 4000,
            background: '#d4edda',
            backdrop: 'rgba(0,0,0,0.7)',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
        // Redirigir después del éxito, si es necesario
        window.location.href = '/administrador_productos';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        Swal.fire({
            title: 'Error',
            text: 'Ocurrió un error al registrar el producto.',
            icon: 'error',
            iconColor: '#ec221f',
            showConfirmButton: false,
            timer: 4000,
            background: '#f8d7da',
            backdrop: 'rgba(0,0,0,0.7)',
            customClass: {
                popup: 'mi-alerta-redondeada'
            }
        });
    });
}

//Modal para detalles
function detallesProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_producto_dettalles', {
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
//Modal para editar
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal
    
    fetch('/api/buscador_producto_edit', {
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
function editarsqlcontenido(idw){
    const id = idw;

    // Obtén los datos
    const temporada = document.getElementById('temporadad').value;
    const tamaño = document.getElementById('tamañod').value;
    const nombre = document.getElementById('nombred').value;
    const descripcion = document.getElementById('descripciond').value;
    const precio_lot = document.getElementById('precio_lotd').value;
    const color = document.getElementById('colord').value;
    const materia = document.getElementById('materiad').value;

    if (!temporada || !tamaño || !nombre || !descripcion || !precio_lot || !color) {
        alert("Por favor, completa todos los campos. (Exeptuando Material)");
        return;  // Detener la ejecución si algún campo está vacío
    }

    //Creae un FormData
    const formData = new FormData();
    formData.append('temporada', temporada);
    formData.append('tamaño', tamaño);
    formData.append('nombre', nombre);
    formData.append('descripcion', descripcion);
    formData.append('precio_lot', precio_lot);
    formData.append('color', color);
    formData.append('materia', materia);
    formData.append('id', id);

    document.getElementById('loading').style.display = 'flex';

    fetch('/actualizar_producto', {
        method: 'POST',
        body: formData 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        ActualizarProducto();
        document.getElementById('loading').style.display = 'none';
/*         alert(data.message); 
        window.location.href = '/administrador_productos'; */
    })
    .catch(error => {
        console.error('Error:', error);
/*         alert("Error al registrar: " + error.message); */
        showServerErrorAlert();
        document.getElementById('loading').style.display = 'none';
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
        window.location.reload();
    })
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