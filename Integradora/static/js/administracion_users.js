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

/*
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tabla_users')
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
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este usuario? (Ya no sera reversible esta operación)");
    
    if (confirmacion){

        // Mostrar la pantalla de carga
        document.getElementById('loading').style.display = 'flex';
    
        // Enviar solo el parámetro 'param' a Flask
        fetch('/eliminar_usuarios', {
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
            alert("Eliminación exitosa");
            window.open('/administrador_user', '_self'); // Redirige después del éxito
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al eliminar: " + error.message); // Mostrar alerta de error
        })
        .finally(() => {
            // Asegurarse de ocultar la pantalla de carga en cualquier caso
            document.getElementById('loading').style.display = 'none';
        });
    }
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
window.onclick = function(event) {
    var modal = document.getElementById("miModal2");
    if (event.target === modal) {
        cerrarModal();
    }
}

//Modal para detalles
function detalleProductos(id) {
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
function editarsqlcontenido(idw){
    const rol = document.getElementById('rol').value;
    const estado = document.getElementById('estado').value;
    const id = idw;

    fetch('/actualizar_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rol: rol,
            estado: estado,
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
        alert(data.message); 
        window.location.href = '/administrador_user';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error al registrar: " + error.message);
    });
}
//Registrar
function registrartemporadao(){
    document.getElementById('loading').style.display = 'flex';

    const formData = {
        name: document.getElementById('name').value,
        lastname: document.getElementById('lastname').value,
        surname: document.getElementById('surname').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };
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
}