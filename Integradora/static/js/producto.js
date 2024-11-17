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

function registrarcomentario(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id');
    let comentario = document.getElementById('nuevo-comentario').value;
    let calif = document.getElementById('califa').value;
    //console.log(id);
    //console.log(calif);
    //console.log(comentario);

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
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        alert("Registro exitoso");
        window.location.reload();
        /*
        RegistrarProducto();
        setTimeout(() => {
            window.location.reload();
            //window.location.href = '/administrador_season'; // Redirige después del éxito
        }, 500);
         */
    })
    .catch(error => {
        console.error('Error:', error);
        //showServerErrorAlert();
        alert("Error al registrar: " + error.message);
    });
}
////Registrar comentrio///////////////////////////
/*
const stars = document.querySelectorAll('.star');

stars.forEach(function(star) {
    star.addEventListener('click', function() {
        const id = this.dataset.id;
        const url = `/producto/like/${id}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
    });
});

stars.forEach(function(star, index){
    star.addEventListener('click', function(){
        for (let i=0; i<=index; i++){
            stars[i].classList.add('checked');
        }
        for (let i=index+1; i<stars.length; i++){
            stars[i].classList.remove('checked');
        }
        punctuation=i;
    });
})
 */
