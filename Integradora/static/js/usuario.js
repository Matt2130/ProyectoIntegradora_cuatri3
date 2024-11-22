function eliminarusuariosolito(param) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este usuario? (Ya no sera reversible esta operación)");
    
    if (confirmacion){

        // Mostrar la pantalla de carga
        document.getElementById('loading').style.display = 'flex';
    
        // Enviar solo el parámetro 'param' a Flask
        fetch('/eliminar_usuario_el_solito', {
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
function editarsqlcontenidousuariosolo(){
    
    const usuario = document.getElementById('usuariod').value;
    const email = document.getElementById('emaild').value;
    const nombre = document.getElementById('nombred').value;
    const apellidop = document.getElementById('apellidopaternod').value;
    const apellidom = document.getElementById('apellidomaternod').value;
    const contraseñanueva = document.getElementById('contraseñanuevad').value;
    const contraseñaanterior = document.getElementById('contraseñaanteriord').value;

    if (!usuario || !email || !nombre || !apellidop || !apellidom || !contraseñaanterior) {
        alert('Por favor, completa todos los campos exepto "Nueva contraseña" de no queres cambiar contraseña.');
        return;  // Detener la ejecución si algún campo está vacío
    }
    // Validación de la nueva contraseña si se proporciona
    if (contraseñanueva) {
        // Expresión regular para validar la contraseña
        const passwordPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

        if (!passwordPattern.test(contraseñanueva)) {
            alert("La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.");
            return;  // Detener la ejecución si la contraseña no cumple con los requisitos
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

    fetch('/actualizar_usuario_solito', {
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
/*         alert(data.message); 
        window.location.href = '/administrador_productos'; */
    })
    .catch(error => {
        console.error('Error:', error);
/*         alert("Error al registrar: " + error.message); */
        showServerErrorAlert();
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
    });
}