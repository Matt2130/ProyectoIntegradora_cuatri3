document.addEventListener('DOMContentLoaded', function() {
    // Verificar el estado de la sesión al cargar la página
    /* 
    fetch('/check_session', { // Solicitud para comprobar el estado de la sesión
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            // Si la sesión no está activa, redirigir a la página de inicio
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Error al comprobar la sesión:', error);
    });
    */
    
    // Escuchar el evento click en el botón de salir
    document.getElementById('salir').addEventListener('click', function() {
        // Realizar la solicitud para cerrar sesión
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¿Estás seguro que quieres cerrar sesión?",
            icon: 'warning',
            iconColor: '#ec221f',
            showCancelButton: true,
            cancelButtonColor: '#d33',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#fed800',
            confirmButtonText: 'Salir',
            background: '#bfbfbf', // Fondo blanco de la alerta
            backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
            customClass: {
                popup: 'mi-alerta-redondeada'  // Clase personalizada
            }
        }).then((result) => {
            if (result.isConfirmed) {
                fetch('/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al cerrar sesión');
                    }
                    return response.json(); // Esperar la respuesta JSON
                })
                .then(data => {
                    // Redirigir a la URL especificada en el JSON de respuesta
                    Secioncerrada()
                    //window.location.reload();
                    //window.location.href = data.redirect; // Cambia aquí según la ruta que desees
                })
                .catch(error => {
                    console.error('Error:', error); // Manejo de errores
                });
            }
        });
    });
});
///////////////
function Secioncerrada() {
    Swal.fire({
        icon: 'success',
        iconColor: '#2b8c4b',
        title: 'Saliendo...',
        text: 'Sesión cerrada',
        timer: 2000,
        showConfirmButton: false,
        background: '#bfbfbf', // Fondo blanco de la alerta
        backdrop: 'rgba(0,0,0,0.7)', // Fondo oscuro con transparencia
        customClass: {
            popup: 'mi-alerta-redondeada'
        }
    }).then(() => {
        window.location.href = '/';
        //window.location.reload();
    });
}