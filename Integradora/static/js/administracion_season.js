document.addEventListener('DOMContentLoaded', function() {
    cargarProductos(1);  // Cargar la primera página de la tabla
});

// Función para cargar productos de una página específica
function cargarProductos(page) {
    fetch('/api/tabla_season_specification?page=' + page)
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

// Buscador para productos
function buscador(page = 1) {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_season?page=' + page, {  // Ahora enviamos 'page' en la URL
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

// Función para manejar la paginación
function paginacion(page) {
    const buscar = document.getElementById('buscador').value;
    if (buscar === '') {
        cargarProductos(page);  // Llamar a cargarProductos si no hay búsqueda
    } else {
        buscador(page);  // Llamar a buscador si hay búsqueda
    }
}

///////////////////////////////////////////////////////////////////////////////////////    
function eliminarProducto(param) {
    //const confirmacion = confirmarEliminacion();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el producto. No podras recuperarlo!",
        icon: 'warning',
        iconColor: '#000000',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#fed800',
        confirmButtonText: 'Eliminar',
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'  // Clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar la pantalla de carga
            document.getElementById('loading').style.display = 'flex';
        
            // Enviar solo el parámetro 'param' a Flask
            fetch('/eliminar_season', {
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
                confirmarEliminacion_eliminar();
                setTimeout(() => {
                    window.open('/administrador_season', '_self'); // Redirige después del éxito
                }, 500);
            })
            .catch(error => {
                console.error('Error:', error);
                showServerErrorAlert();
                //alert("Error al eliminar: " + error.message); // Mostrar alerta de error
            })
            .finally(() => {
                // Asegurarse de ocultar la pantalla de carga en cualquier caso
                document.getElementById('loading').style.display = 'none';
            });
        }
    });
}

/*
function buscador() {
    const buscar = document.getElementById('buscador').value;

    fetch('/api/buscador_season', {
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
 */
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
function registrartemporadao(){
    const temporada = document.getElementById('temporada').value;

    if (!temporada) {
        alert("Por favor, completa el campo de temporada.");
        return;  // Detener la ejecución si el campo 'temporada' está vacío
    }

    fetch('/registrar_season', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temporada: temporada
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        RegistrarProducto();
        setTimeout(() => {
            window.location.href = '/administrador_season'; // Redirige después del éxito
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        showServerErrorAlert();
        //alert("Error al registrar: " + error.message);
    });
}
//Modal para edición
function editarProducto(id) {
    var modal = document.getElementById("miModal2");
    modal.style.display = "block"; // Muestra el modal

    fetch('/api/buscador_season_edit', {
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
//Edicion en la base de datos
function editarsqltemporada(idw){
    const season = document.getElementById('temporadad').value;
    const id = idw;

    if (!season) {
        alert("Por favor, completa el campo de temporada.");
        return;  // Detener la ejecución si el campo 'temporada' está vacío
    }

    fetch('/actualizar_temporada', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            season: season,
            id:id
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        //alert(data.message); 
        ActualizarProducto();
        setTimeout(() => {
            window.location.href = '/administrador_season'; // Redirige después del éxito
        }, 1000);
    })
    .catch(error => {
        console.error('Error:', error);
        showServerErrorAlert();
        //alert("Error al registrar: " + error.message);
    });
}

//Funcion de eliminacion exitos
function confirmarEliminacion_eliminar(){
    Swal.fire({
        title: 'Eliminado',
        text: 'Producto eliminado correctamente',
        icon: 'success',
        iconColor: '#2b8c4b',
        background: '#bfbfbf',
        showConfirmButton: false,
        backdrop: 'rgba(0,0,0,0.7)',
        timer: 4000, // La alerta de éxito se cerrará automáticamente
        customClass: {
            popup: 'mi-alerta-redondeada'  // Clase personalizada
        }
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
//fghjkl
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
    })
}