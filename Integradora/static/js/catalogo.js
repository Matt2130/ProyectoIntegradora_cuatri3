document.addEventListener('DOMContentLoaded', function() {
    mostrarProductos();  // Cargar la primera página de productos al cargar la página
});
// Función para mostrar productos con paginación
function mostrarProductos(page = 1) {
    fetch(`/api/mostrador_productos?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();  // Recibe el HTML para actualizar el catálogo
        })
        .then(data => {
            document.getElementById('catalogo').innerHTML = data;  // Actualiza el contenedor con los productos
        })
        .catch(error => console.error('Error:', error));
}

/*
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/mostrador_productos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red: ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('catalogo').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});
 */
//////////////////////////////////////////////////////////////////////////////////////////
/*
function buscar_producto_select() {
    //console.log(147865485);
    const categoria = document.getElementById('categoria').value;
    const buscar = document.getElementById('buscador').value;

    fetch('/api/mostrador_productos_buscados', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            buscar: buscar,
            categoria:categoria
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text();
    })
    .then(html => {
        // Muestra los resultados HTML en el contenedor
        const resultsContainer = document.getElementById('catalogo');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
     
}
 */

function buscar_producto_select(page = 1) {
    const categoria = document.getElementById('categoria').value;
    const buscar = document.getElementById('buscador').value;

    fetch('/api/mostrador_productos_buscados?page=' + page, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            buscar: buscar,
            categoria: categoria
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.text();  // Recibe el HTML para actualizar la tabla
    })
    .then(html => {
        // Actualiza el contenido del catálogo
        const resultsContainer = document.getElementById('catalogo');
        resultsContainer.innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
