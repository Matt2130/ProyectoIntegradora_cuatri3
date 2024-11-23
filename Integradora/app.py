from flask import Flask, make_response, redirect, url_for, render_template, session, request, jsonify, Response
from sqlalchemy import create_engine, text
from functools import wraps
import os
from werkzeug.security import generate_password_hash, check_password_hash
#Se eliminara pero es para hacer pruebas
import time


#app = Flask(__name__)
app = Flask(__name__, static_folder="static")

# Establecer la clave secreta
app.secret_key = '12345'  # Cambia esto por una clave única

#Conexión
engine = None

##Decorador de Autorización
def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'permiso_usuario' not in session:
                return redirect(url_for('inicio_usuario'))
            if session['permiso_usuario'] != role:
                return redirect(url_for('/')) 
            return f(*args, **kwargs)
        return wrapped
    return decorator

#Función para iniciar la base de datos
def init_db():
    global engine
    if engine is None:
        engine = create_engine('mysql+pymysql://root:@localhost/integradora')
        #mysql+pymysql://<usuario>:<contraseña>@<host>/<nombre_base_de_datos>
        #Manuel
        #mysql+pymysql://root:'pass123'@localhost/integradora
        #Mario
        #mysql+pymysql://root:@localhost/integradora
########################################################################################################################################

#Funciones a llamar desde la web#####################################################################################################
@app.route('/check_session', methods=['GET'])
def check_session():
    if 'permiso_usuario' in session:
        return jsonify({"status": "active"}), 200
    return jsonify({"status": "inactive"}), 401

@app.route('/api/contactos')
def contactos():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone FROM contacts;"))
            contactos = result.fetchall()
            nombre_columnas = result.keys()
            html = ""

            for redes in contactos:
                html += '<div class="contacto_contenedor">'
                for url, nombre in zip(redes, nombre_columnas):
                    if url:
                        if nombre == 'Email':
                            link = f"mailto:{url}"
                        elif nombre == 'Whatsapp':
                            link = f"https://wa.me/{url}"
                        elif nombre == 'Phone':
                            link = f"tel:{url}"
                        else:
                            # Link para redes sociales como Facebook, Instagram, etc.
                            link = url
                        
                        html += f"""
                        <div class="elementos">
                            <a target="_blank" href="{link}">
                                <img src="static/image/{nombre}.svg" alt="{nombre}" class="{nombre}">
                            </a>
                        </div>
                        """
                html += '</div><hr>'

            return Response(html, mimetype='text/html')
    except Exception as e:
        print(e)
        return Response("Error 404", mimetype='text/html')

@app.route('/api/texto_vision_mision')
def texto_mision_vision():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe FROM content WHERE content.Title!="Valores" AND content.Title!="Mision" AND content.Title!="Vision";'))
            contenido = result.fetchall()
            html = ""

            for titulo, descripcion in contenido:
                html += '<div class="valores_derechos">'
                html += f"""
                    <h2>{titulo}</h2>
                    <p>{descripcion}</p> 
                """
                html += '</div><br>'

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/texto_valores')
def texto_valores():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe FROM content WHERE content.Title="Valores" OR content.Title="Misión" OR content.Title="Visión";'))
            contenido = result.fetchall()
            html = ""

            for titulo, descripcion in contenido:
                html += '<div class="valores_derechos">'
                html += f"""
                    <h2>{titulo}</h2>
                    <p>{descripcion}</p> 
                """
                html += '</div><br>'

            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/mostrador_productos')
def mostrador_productos():
    page = int(request.args.get('page', 1))  # Obtener el número de página desde los parámetros de la URL
    limit = 20  # Número de productos por página
    offset = (page - 1) * limit  # Calcular el desplazamiento para la consulta

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta para obtener los productos con paginación
            sql_query = """
                SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product 
                FROM products
                LIMIT :limit OFFSET :offset;
            """
            result = connection.execute(text(sql_query), {"limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Consulta para contar el total de productos
            count_query = "SELECT COUNT(*) FROM products"
            result_count = connection.execute(text(count_query))
            total_products = result_count.scalar()  # Número total de productos
            total_pages = (total_products + limit - 1) // limit  # Calcular el total de páginas

            html = ""

            for info in contenido:
                direccion_imagen = url_for('static', filename=f'image/imagenes_productos/{info[0]}', _external=True)
                html += f"""
                        <div class="producto">
                            <a href="/producto?id={info[4]}">
                                <div id="imagen">
                                    <img src="{direccion_imagen}" alt="{info[0]}">
                                </div>
                                <div id="info">
                                    <h3 id="nombre-producto">{info[1]}</h3>
                                    <p id="color-modelo">{info[2]}</p>
                                    <strong id="precio">${info[3]}</strong>
                                </div>
                            </a>
                        </div>
                """

            # Agregar los botones de paginación
            html += """
                <div class="paginacion">
            """
            # Mostrar botón "Anterior" si no es la primera página
            if page > 1:
                html += f'<a href="#" onclick="mostrarProductos({page-1})">Anterior</a>'
            # Mostrar botón "Siguiente" si no es la última página
            if page < total_pages:
                html += f'<a href="#" onclick="mostrarProductos({page+1})">Siguiente</a>'
            html += """
                </div>
            """

            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

#Tablas
@app.route('/api/tabla_productos')
def tabla_productos():
    # Obtener el número de página desde los parámetros de la URL (por defecto es 1)
    page = int(request.args.get('page', 1))
    limit = 10  # Número de elementos por página
    offset = (page - 1) * limit  # Calcular el desplazamiento para la consulta

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta SQL con LIMIT y OFFSET para la paginación
            sql_query = """
                SELECT products.Name, products.Model, products.Size, products.Material_composition, products.Price_per_unit, products.Color, products.Id_product
                FROM products
                LIMIT :limit OFFSET :offset;
            """
            result = connection.execute(text(sql_query), {"limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Contar el total de registros para calcular el número total de páginas
            result_count = connection.execute(text("SELECT COUNT(*) FROM products"))
            total_products = result_count.scalar()  # Número total de registros
            total_pages = (total_products + limit - 1) // limit  # Número total de páginas

            # Generar el HTML para la tabla
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Modelo</th>
                        <th>Tamaño</th>
                        <th>Material de composición</th>
                        <th>Precio</th>
                        <th>Color</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="detallesProducto({info[6]})" class="detalles"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-details" viewBox="0 0 16 16">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                </svg></button>
                            <button onclick="editarProducto({info[6]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            # Agregar los botones de paginación
            html += """
                <div class="paginacion">
            """
            # Mostrar botón "Anterior" si no es la primera página
            if page > 1:
                html += f'<a href="#" onclick="cargarProductos({page-1})">Anterior</a>'
            # Mostrar botón "Siguiente" si no es la última página
            if page < total_pages:
                html += f'<a href="#" onclick="cargarProductos({page+1})">Siguiente</a>'
            html += """
                </div>
            """

            # Devolver el HTML generado
            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_season_specification')
def tabla_season_specification():
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = '''
                SELECT season_specification.season, season_specification.Id_season
                FROM season_specification
                LIMIT :limit OFFSET :offset;
            '''
            result = connection.execute(
                text(sql_query),
                {"limit": limit, "offset": offset}
            )
            contenido = result.fetchall()

            result_count = connection.execute(
            text('SELECT COUNT(*) FROM season_specification'))

            total_seasons = result_count.scalar()
            total_pages = (total_seasons + limit - 1) // limit

            html = """
            <table>
                <thead>
                    <tr>
                        <th>Temporada</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>
                            <button onclick="editarProducto({info[1]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="PantallaeliminacionProducto({info[1]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            html += """
                <div class="paginacion">
            """
            if page > 1:
                html += f"""
                    <a href="#" onclick="paginacion({page-1})">Anterior</a>
                """
            if page < total_pages:
                html += f"""
                    <a href="#" onclick="paginacion({page+1})">Siguiente</a>
                """
            html += "</div>"

            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/tabla_contact')
def tabla_contact():
    try:
        init_db()
        with engine.connect() as connection:
            # Realizar la consulta
            result = connection.execute(text("""
                SELECT Facebook, Instagram, Tik_tok, Email, Twitter, Whatsapp, Phone, Id_contact 
                FROM contacts;
            """))
            contactos = result.fetchall()
            nombre_columnas = result.keys()

        if contactos:
            html = ""
            for redes in contactos:
                id_contact = redes[-1]  # Id_contact como último elemento
                html += '<div class="contacto_contenedor">'
                for url, nombre in zip(redes, nombre_columnas):
                    # Excluir Id_contact del HTML
                    if nombre == "Id_contact":
                        continue
                    
                    if nombre == 'Email':
                        link = f"mailto:{url}"
                    elif nombre == 'Whatsapp':
                        link = f"https://wa.me/{url}"
                    elif nombre == 'Phone':
                        link = f"tel:{url}"
                    else:
                        link = url  # Redes sociales como Facebook, Instagram, etc.

                    # Generar los elementos visuales
                    html += f"""
                    <div class="elementos">
                        <a target="_blank" href="{link}">
                            <img src="static/image/{nombre}.svg" alt="{nombre}" class="{nombre}">
                        </a>
                    </div>
                    """
                html += f"""
                <hr>
                <br>
                <button onclick="editarProducto({id_contact})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                    </svg></button>
                <button onclick="eliminarProducto({id_contact})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                    </svg></button>
                """
                html += '</div>'
        else:
            # Si no hay contactos, mostrar botón de registro
            html = """
            <div class="arriba">
                <button id="abrirModal" onclick="abrirModal()">Registrar</button>
            </div>
            """

        return Response(html, mimetype='text/html')
    except Exception as e:
        return Response(f"Error 404: {str(e)}", mimetype='text/html')

@app.route('/api/tabla_content')
def tabla_content():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe, content.Id_contenido FROM content;'))
            contenido = result.fetchall()
            
            html = ""
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                            </svg></button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                            </svg></button>
                    </div>
                """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

@app.route('/api/tabla_users')
def tabla_users():
    # Obtener el número de página de los parámetros de la URL (por defecto es 1)
    page = int(request.args.get('page', 1))
    limit = 10  # Número de elementos por página
    offset = (page - 1) * limit  # Calcular el desplazamiento para la consulta

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta SQL con LIMIT y OFFSET para la paginación
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Id_user
                FROM users
                LIMIT :limit OFFSET :offset;
            """
            result = connection.execute(text(sql_query), {"limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Contar el total de registros para calcular el número total de páginas
            result_count = connection.execute(text("SELECT COUNT(*) FROM users"))
            total_users = result_count.scalar()  # Número total de registros
            total_pages = (total_users + limit - 1) // limit  # Número total de páginas

            # Generar el HTML para la tabla
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Correo</th>
                        <th>Nombre</th>
                        <th>Apellido Paterno</th>
                        <th>Apellido Materno</th>
                        <th>Rol</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="detallesProducto({info[6]})" class="detalles"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-details" viewBox="0 0 16 16">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                </svg></button>
                            <button onclick="editarProducto({info[6]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="PantallaeliminacionProducto({info[6]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>   
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            # Agregar los botones de paginación
            html += """
                <div class="paginacion">
            """
            # Mostrar botón "Anterior" si no es la primera página
            if page > 1:
                html += f'<button onclick="cargarUsuarios({page-1})">Anterior</button>'
            # Mostrar botón "Siguiente" si no es la última página
            if page < total_pages:
                html += f'<button onclick="cargarUsuarios({page+1})">Siguiente</button>'
            html += """
                </div>
            """

            # Devolver el HTML generado
            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/contenido_inicio_administracion')
def contenido_inicio_administracion():
    try:
        init_db()
        with engine.connect() as connection:
            result = connection.execute(text('SELECT content.Title, content.Describe, content.Id_contenido FROM content;'))
            contenido = result.fetchall()
            
            html = "Proximamente"
            '''
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                            </svg></button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                            </svg></button>  
                    </div>
                """
            '''
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')

#Buscador tablas
@app.route('/api/buscador_content', methods=['POST'])
def buscador_content():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')

    try:
        init_db()
        with engine.connect() as connection:
            
            sql_query = """
                SELECT content.Title, content.Describe, content.Id_contenido 
                FROM content 
                WHERE content.Title LIKE :buscar OR content.Describe LIKE :buscar
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%"})
            contenido = result.fetchall()

            # Construcción de la tabla HTML con los resultados
            html = ""
            for info in contenido:
                html += f"""
                    <div class="content" onclick="toggleExpand(event, this)">
                        <h2>{info[0]}</h2>
                        <p>{info[1]}</p>
                        <button onclick="editarProducto({info[2]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                            </svg></button>
                        <button onclick="eliminarProducto({info[2]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                            </svg></button>
                    </div>
                """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_season', methods=['POST'])
def buscador_season():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = '''
                SELECT season_specification.season, season_specification.Id_season
                FROM season_specification
                WHERE season_specification.season LIKE :buscar
                LIMIT :limit OFFSET :offset;
            '''
            result = connection.execute(
                text(sql_query),
                {"buscar": f"%{buscar}%", "limit": limit, "offset": offset}
            )
            contenido = result.fetchall()

            result_count = connection.execute(
                text('SELECT COUNT(*) FROM season_specification WHERE season_specification.season LIKE :buscar'),
                {"buscar": f"%{buscar}%"}
            )
            total_seasons = result_count.scalar()
            total_pages = (total_seasons + limit - 1) // limit

            html = """
            <table>
                <thead>
                    <tr>
                        <th>Temporada</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>
                            <button onclick="editarProducto({info[1]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="PantallaeliminacionProducto({info[1]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>   
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            html += """
                <div class="paginacion">
            """
            if page > 1:
                html += f"""
                    <a href="#" onclick="paginacion({page-1})">Anterior</a>
                """
            if page < total_pages:
                html += f"""
                    <a href="#" onclick="paginacion({page+1})">Siguiente</a>
                """
            html += "</div>"

            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_users', methods=['POST'])
def buscador_users():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')
    page = int(request.args.get('page', 1))  # Página actual
    limit = 10  # Número de elementos por página
    offset = (page - 1) * limit  # Calcular desplazamiento

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta SQL con búsqueda, límite y desplazamiento
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Id_user
                FROM users
                WHERE users.User LIKE :buscar
                OR users.Email LIKE :buscar
                OR users.Name LIKE :buscar
                OR users.Surname LIKE :buscar
                OR users.Lastname LIKE :buscar
                OR users.Rol LIKE :buscar
                OR users.Estado LIKE :buscar
                LIMIT :limit OFFSET :offset;
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%", "limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Contar el total de registros que coinciden con la búsqueda
            count_query = """
                SELECT COUNT(*) 
                FROM users
                WHERE users.User LIKE :buscar
                OR users.Email LIKE :buscar
                OR users.Name LIKE :buscar
                OR users.Surname LIKE :buscar
                OR users.Lastname LIKE :buscar
                OR users.Rol LIKE :buscar
                OR users.Estado LIKE :buscar;
            """
            total_count = connection.execute(text(count_query), {"buscar": f"%{buscar}%"}).scalar()
            total_pages = (total_count + limit - 1) // limit  # Total de páginas

            # Generar el HTML para la tabla
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Correo</th>
                        <th>Nombre</th>
                        <th>Apellido paterno</th>
                        <th>Apellido Materno</th>
                        <th>Rol</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="detallesProducto({info[6]})" class="detalles"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-details" viewBox="0 0 16 16">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                </svg></button>
                            <button onclick="editarProducto({info[6]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="PantallaeliminacionProducto({info[6]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>  
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            # Agregar botones de paginación
            html += """
                <div class="paginacion">
            """
            if page > 1:
                html += f'<button onclick="buscarUsuarios(\'{buscar}\', {page-1})">Anterior</button>'
            if page < total_pages:
                html += f'<button onclick="buscarUsuarios(\'{buscar}\', {page+1})">Siguiente</button>'
            html += """
                </div>
            """

            # Devolver el HTML generado
            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_productos', methods=['POST'])
def buscador_productos():
    informacion = request.get_json()
    buscar = informacion.get('buscar', '')
    page = int(request.args.get('page', 1))  # Obtener el número de página (por defecto es 1)
    limit = 10  # Número de productos por página
    offset = (page - 1) * limit  # Calcular el desplazamiento para la consulta

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Name, products.Model, products.Size, products.Material_composition, products.Price_per_unit, products.Color, products.Id_product
                FROM products
                INNER JOIN season_specification ON products.FK_id_season = season_specification.Id_season
                INNER JOIN users ON products.FK_Id_user = users.Id_user
                WHERE 
                    products.Model LIKE :buscar OR
                    season_specification.season LIKE :buscar OR
                    products.Size LIKE :buscar OR
                    products.Name LIKE :buscar OR
                    products.Description LIKE :buscar OR
                    products.Price_per_unit LIKE :buscar OR
                    products.Color LIKE :buscar OR
                    users.User LIKE :buscar
                LIMIT :limit OFFSET :offset;
            """
            result = connection.execute(text(sql_query), {"buscar": f"%{buscar}%", "limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Contar el total de registros para calcular el número total de páginas
            count_query = """
                SELECT COUNT(*) 
                FROM products
                INNER JOIN season_specification ON products.FK_id_season = season_specification.Id_season
                INNER JOIN users ON products.FK_Id_user = users.Id_user
                WHERE 
                    products.Model LIKE :buscar OR
                    season_specification.season LIKE :buscar OR
                    products.Size LIKE :buscar OR
                    products.Name LIKE :buscar OR
                    products.Description LIKE :buscar OR
                    products.Price_per_unit LIKE :buscar OR
                    products.Color LIKE :buscar OR
                    users.User LIKE :buscar;
            """
            result_count = connection.execute(text(count_query), {"buscar": f"%{buscar}%"})
            total_products = result_count.scalar()  # Número total de registros
            total_pages = (total_products + limit - 1) // limit  # Número total de páginas

            # Generar el HTML para la tabla
            html = """
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Modelo</th>
                        <th>Tamaño</th>
                        <th>Material de composición</th>
                        <th>Precio</th>
                        <th>Color</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
            """
            for info in contenido:
                html += f"""
                    <tr>
                        <td>{info[0]}</td>
                        <td>{info[1]}</td>
                        <td>{info[2]}</td>
                        <td>{info[3]}</td>
                        <td>{info[4]}</td>
                        <td>{info[5]}</td>
                        <td>
                            <button onclick="detallesProducto({info[6]})" class="detalles"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-details" viewBox="0 0 16 16">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                </svg></button>
                            <button onclick="editarProducto({info[6]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg></button>
                            <button onclick="eliminarProducto({info[6]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                </svg></button>  
                        </td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

            # Agregar los botones de paginación
            html += """
                <div class="paginacion">
            """
            # Mostrar botón "Anterior" si no es la primera página
            if page > 1:
                html += f'<a href="#" onclick="buscador({page-1})">Anterior</a>'
            # Mostrar botón "Siguiente" si no es la última página
            if page < total_pages:
                html += f'<a href="#" onclick="buscador({page+1})">Siguiente</a>'
            html += """
                </div>
            """

            # Devolver el HTML generado
            return Response(html, mimetype='text/html')

    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/comentarios_producto', methods=['POST','GET'])
def comentarios_producto():
    informacion = request.get_json()
    id = informacion.get('id')
    
    #print(id)
    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, comments.Punctuation, comments.Comment, users.Id_user, comments.Id_coment
                FROM products 
                INNER JOIN comments ON products.Id_product=comments.FK_Id_product 
                INNER JOIN users ON comments.FK_Id_customer=users.Id_user 
                WHERE  products.Id_product=:id;
            """
            result = connection.execute(text(sql_query), {"id": id})
            contenido = result.fetchall()
            
            html = """
            
            """
            for info in contenido:
                html += f"""
                <div class="comentario-usuario">
                    <p>{info[0]}</p>
                    Puntuación:{info[1]}
                    """
                if session['id_usuario'] == info[3]:
                    html += f"""
                    <button onclick="editarComentario({info[4]})" class="editar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-edit" viewBox="0 0 16 16">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                        </svg></button>
                    <button onclick="eliminarComentario({info[4]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                        </svg></button>
                    """
                elif session['permiso_admin'] == True:
                    html += f"""
                    <button onclick="eliminarComentario({info[4]})" class="eliminar"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="icon-del" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                        </svg></button>
                    """
                html +=f"""
                </div>
                <div class="comentario-texto">
                    <div id="comentario">
                        {info[2]}
                    </div>
                </div>
                <hr>
                """
            html += """
                
            """
            
            return Response(html, mimetype='text/html')
    except:
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/mostrador_productos_buscados', methods=['POST', 'GET'])
def mostrador_productos_buscados():
    try:
        data = request.json
        buscar = data.get('buscar', '')  # Obtiene el valor de 'buscar'
        categoria = data.get('categoria', '')
        page = int(request.args.get('page', 1))  # Número de página, por defecto 1
        limit = 20  # Número de productos por página
        offset = (page - 1) * limit  # Calcular el desplazamiento para la consulta

        init_db()
        with engine.connect() as connection:
            # Definir la consulta según la categoría
            match categoria:
                case "Model":
                    sql_query = """
                        SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product
                        FROM products WHERE products.Model LIKE :coso LIMIT :limit OFFSET :offset;
                    """
                case "Size":
                    sql_query = """
                        SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product
                        FROM products WHERE products.Size LIKE :coso LIMIT :limit OFFSET :offset;
                    """
                case "Name":
                    sql_query = """
                        SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product
                        FROM products WHERE products.Name LIKE :coso LIMIT :limit OFFSET :offset;
                    """
                case "Description":
                    sql_query = """
                        SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product
                        FROM products WHERE products.Description LIKE :coso LIMIT :limit OFFSET :offset;
                    """
                case "Color":
                    sql_query = """
                        SELECT products.url_imagen, products.Name, products.Color, products.Price_per_unit, products.Id_product
                        FROM products WHERE products.Color LIKE :coso LIMIT :limit OFFSET :offset;
                    """
                case _:
                    return Response("Error 404", mimetype='text/html')

            # Ejecutar la consulta para obtener los productos
            result = connection.execute(text(sql_query), {"coso": f"%{buscar}%", "limit": limit, "offset": offset})
            contenido = result.fetchall()

            # Consultar el número total de productos que coinciden con la búsqueda
            count_query = """
                SELECT COUNT(*) FROM products WHERE
                    products.Model LIKE :coso OR
                    products.Size LIKE :coso OR
                    products.Name LIKE :coso OR
                    products.Description LIKE :coso OR
                    products.Color LIKE :coso;
            """
            result_count = connection.execute(text(count_query), {"coso": f"%{buscar}%"})
            total_products = result_count.scalar()  # Total de productos encontrados
            total_pages = (total_products + limit - 1) // limit  # Calcular número total de páginas

            # Generar el HTML para los productos
            html = ""
            for info in contenido:
                direccion_imagen = url_for('static', filename=f'image/imagenes_productos/{info[0]}', _external=True)
                html += f"""
                    <div class="producto">
                        <a href="/producto?id={info[4]}">
                            <div id="imagen">
                                <img src="{direccion_imagen}" alt="{info[0]}">
                            </div>
                            <div id="info">
                                <h3 id="nombre-producto">{info[1]}</h3>
                                <p id="color-modelo">{info[2]}</p>
                                <strong id="precio">${info[3]}</strong>
                            </div>
                        </a>
                    </div>
                """

            # Agregar los botones de paginación
            html += """
                <div class="paginacion">
            """
            # Botón "Anterior"
            if page > 1:
                html += f'<a href="#" onclick="buscar_producto_select({page-1})">Anterior</a>'
            # Botón "Siguiente"
            if page < total_pages:
                html += f'<a href="#" onclick="buscar_producto_select({page+1})">Siguiente</a>'
            html += """
                </div>
            """

            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error: {e}")
        return Response("Error 404", mimetype='text/html')

#Registros
@app.route('/registro_usuario', methods=['POST'])
def signup():
    init_db()

    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    surname = data.get('surname')

    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User FROM users WHERE users.Email=:correo;
            """
            result = connection.execute(text(sql_query), {"correo": email})
            contenido = result.fetchone()
            if not contenido:
                
                # Iniciar una transacción
                connection.execute(text("START TRANSACTION;"))

                sql_query = """
                    INSERT INTO users (User, Password, Email, Name, Surname, Lastname, Rol, Estado)
                    VALUES (:username, :password, :email, :name, :surname, :lastname, 'cliente', 'Activo')
                """
                print(f"Ejecutando consulta: {sql_query}")

                # Ejecutar la consulta
                connection.execute(text(sql_query), {
                    "username": username,
                    "password": password,
                    "email": email,
                    "name": name,
                    "surname": surname,
                    "lastname": lastname
                })

                # Finalizar transacción
                connection.execute(text("COMMIT;"))
            else:
                return jsonify({"message": "Correo ya registrado"}), 400
        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registro_usuario_administrador', methods=['POST'])
def registro_usuario_administrador():
    init_db()

    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    surname = data.get('surname')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga
    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User FROM users WHERE users.Email=:correo;
            """
            result = connection.execute(text(sql_query), {"correo": email})
            contenido = result.fetchone()
            if not contenido:
                
                # Iniciar una transacción
                connection.execute(text("START TRANSACTION;"))

                sql_query = """
                    INSERT INTO users (User, Password, Email, Name, Surname, Lastname, Rol, Estado)
                    VALUES (:username, :password, :email, :name, :surname, :lastname, 'administrador', 'Activo')
                """
                print(f"Ejecutando consulta: {sql_query}")

                # Ejecutar la consulta
                connection.execute(text(sql_query), {
                    "username": username,
                    "password": password,
                    "email": email,
                    "name": name,
                    "surname": surname,
                    "lastname": lastname
                })

                # Finalizar transacción
                connection.execute(text("COMMIT;"))
            else:
                return jsonify({"message": "Correo ya registrado"}), 400
        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_contenido', methods=['POST'])
def registrar_contenido():
    init_db()

    data = request.get_json()
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_check = """
            SELECT 1 FROM content WHERE content.Title = :titulo;
            """
            result = connection.execute(text(sql_check), {
                "titulo": titulo,
            }).fetchone()
            
            if result:
                return jsonify({"message": "Título ya registrado, favor de cambiarlo"}), 400
            
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `content` (`Title`, `Describe`)
                VALUES (:titulo, :descripcion);
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "titulo": titulo,
                "descripcion": descripcion
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))
            
        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_comentario', methods=['POST'])
def registrar_comentario():
    init_db()

    data = request.get_json()
    id_produto = data.get('id')
    calificacion = data.get('calificacion')
    comentario = data.get('comentario')

    try:
        with engine.connect() as connection:
            # Validar si ya existe un comentario
            sql_query = """
                SELECT 1 FROM comments WHERE FK_Id_product = :id_producto AND FK_Id_customer = :id_usuario;
            """
            result = connection.execute(text(sql_query), {
                "id_producto": id_produto,
                "id_usuario": session['id_usuario']
            }).fetchone()

            if result:
                return jsonify({"message": f"Ya existe un comentario registrado para este producto."}), 400

            # Registrar nuevo comentario
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `comments` (`Punctuation`, `Comment`, `FK_Id_customer`, `FK_Id_product`) 
                VALUES (:calificacion, :comentario, :id_usuario, :id_produto);
            """
            connection.execute(text(sql_query), {
                "calificacion": calificacion,
                "comentario": comentario,
                "id_usuario": session['id_usuario'],
                "id_produto": id_produto,
            })

            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Comentario registrado exitosamente."}), 200

    except Exception as e:
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))
        return jsonify({"message": f"Error al registrar el comentario: {str(e)}"}), 500

@app.route('/registrar_contactos', methods=['POST'])
def registrar_contactos():
    init_db()

    data = request.get_json()
    facebook = data.get('facebook')
    instagram = data.get('instagram')
    tik_tok = data.get('tik_tok')
    email = data.get('email')
    twitter = data.get('twitter')
    whatsapp = data.get('whatsapp')
    phone = data.get('phone')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `contacts` (`Facebook`, `Instagram`, `Tik_tok`, `Email`, `Twitter`, `Whatsapp`, `Phone`) 
                VALUES (:facebook, :instagram, :tik_tok, :email, :twitter, :whatsapp, :phone);
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "facebook": facebook,
                "instagram": instagram,
                "tik_tok": tik_tok,
                "email": email,
                "twitter": twitter,
                "whatsapp": whatsapp,
                "phone": phone
            })

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_season', methods=['POST'])
def registrar_season():
    init_db()

    data = request.get_json()
    temporada = data.get('temporada')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga
    
    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                INSERT INTO `season_specification` (`season`) VALUES (:temporada);
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "temporada": temporada
            })

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    init_db()

    # Captura los datos del formulario
    modelo = request.form.get('modelo')
    temporada = request.form.get('temporada')
    tamaño = request.form.get('tamaño')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio_lot = request.form.get('precio_lot')
    color = request.form.get('color')
    materia = request.form.get('materia')
    

    try:
        # Guardar la imagen
        image = request.files.get('image')
        if image and image.filename.endswith(('.png', '.jpg', '.jpeg')):
            unique_filename = f"{modelo}.png"
            image_path = os.path.join("Integradora","static", "image", "imagenes_productos", unique_filename)
            #image_path = f"static/image/imagenes_productos/{unique_filename}"
            
            '''
            image_dir = os.path.join("static", "image", "imagenes_productos")

            # Verificar si la carpeta existe
            if not os.path.exists(image_dir):
                # Crear la carpeta (y subcarpetas si no existen)
                os.makedirs(image_dir)
            # Generar la ruta completa de la imagen
            unique_filename = f"{modelo}.png"
            image_path = os.path.join(image_dir, unique_filename)
            '''
            """
            #Coso opara ver donde esta guardando las imagenes cuando truene la funcion
            import os
            image_dir = os.path.dirname(image_path)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            """
            
            image.save(image_path)
            #return jsonify({"message": "Registro exitoso"}), 200

            with engine.connect() as connection:
                # Iniciar transacción
                connection.execute(text("START TRANSACTION;"))

                sql_query = """
                INSERT INTO `products` (`Material_composition`, `Model`, `FK_id_season`, `Size`, `Name`, `Description`, `Price_per_unit`, `Color`, `url_imagen`, `FK_Id_user`) 
                VALUES (:materia, :modelo, :temporada, :tamaño, :nombre, :descripcion, :precio_lot, :color, :image_path, :user_id);
                """

                # Ejecutar consulta con la ruta absoluta
                connection.execute(text(sql_query), {
                    "materia": materia,
                    "modelo": modelo,
                    "temporada": temporada,
                    "tamaño": tamaño,
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio_lot": precio_lot,
                    "color": color,
                    "image_path": unique_filename,  # Ruta absoluta
                    "user_id": session['id_usuario']
                })

                # Confirmar transacción
                connection.execute(text("COMMIT;"))

            return jsonify({"message": "Registro exitoso"}), 200
        else:
            return jsonify({"message": "El archivo debe ser una imagen válida (.png, .jpg, .jpeg)"}), 400
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500
    
#Eliminación
@app.route('/eliminar_season', methods=['POST'])
def eliminar_season():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')  # ID de la temporada a eliminar
    nueva_temporada = identificador.get('temporada')  # Nueva temporada para los productos

    if not id or not nueva_temporada:
        return jsonify({"message": "Faltan parámetros requeridos."}), 400

    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))
            
            # Actualizar los productos para que apunten a la nueva temporada
            sql_update = """
                UPDATE `products` 
                SET `FK_id_season` = :nueva_temporada 
                WHERE `FK_id_season` = :id;
            """
            update_result = connection.execute(
                text(sql_update), 
                {"id": id, "nueva_temporada": nueva_temporada}
            )

            # Eliminar la temporada original
            sql_delete = """
                DELETE FROM season_specification 
                WHERE `Id_season` = :id;
            """
            connection.execute(text(sql_delete), {"id": id})

            # Confirmar la transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminación exitosa y productos reasignados."}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_usuarios', methods=['POST'])
def eliminar_usuarios():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    user_new = identificador.get('nuevo_user')
    
    if id==session['id_usuario']:
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE products SET products.FK_Id_user=:user_new WHERE products.FK_Id_user=:identificados;
            """

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "user_new":user_new,
                "identificados": id
            })
            
            sql_query = """
                DELETE FROM users WHERE `users`.`Id_user`=:identificados;
            """

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_contenido', methods=['POST'])
def eliminar_contenido():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM content WHERE `content`.`Id_contenido`=:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_contacto', methods=['POST'])
def eliminar_contacto():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM contacts WHERE `contacts`.`Id_contact` =:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM products WHERE `products`.`Id_product` =:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500

@app.route('/eliminar_usuario_el_solito', methods=['POST'])
def eliminar_usuario_el_solito():
    init_db()
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga
    if 'id_usuario' not in session:
        return jsonify({"message": "No se encontró un usuario en la sesión"}), 400
    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                DELETE FROM users WHERE `users`.`Id_user`=:identificados;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "identificados": session['id_usuario']
            })

            session.clear()

            session['inicio_cesion'] = False
            session['permiso_admin'] = False
    
            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500
    
@app.route('/eliminar_comentario_producto', methods=['POST'])
def eliminar_comentario_producto():
    init_db()

    identificador = request.get_json()
    id = identificador.get('parametro')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                SELECT comments.FK_Id_customer
                FROM comments
                WHERE  comments.Id_coment=:id;
            """
            result = connection.execute(text(sql_query), {"id": id})
            contenido = result.fetchone()
            if contenido[0] == session['id_usuario'] or session['permiso_admin'] == True:
                
                # Iniciar una transacción
                connection.execute(text("START TRANSACTION;"))

                sql_query = """
                    DELETE FROM comments WHERE `comments`.`Id_coment`=:identificados;
                """

                # Ejecutar la consulta
                connection.execute(text(sql_query), {
                    "identificados": id
                })

                # Finalizar transacción
                connection.execute(text("COMMIT;"))
            else:
                return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500
        return jsonify({"message": "Eliminacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al eliminar: {str(e)}"}), 500
    
#Solicitar datos para edición
@app.route('/api/buscador_content_edit', methods=['POST'])
def buscador_content_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT content.Title, content.Describe, content.Id_contenido 
                FROM content 
                WHERE content.Id_contenido=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Edición de contenido</h1>
            <br>
            <label for="titulo">
                <h2>Titulo</h2>
                <br>
                <input type="text" id="tituloedit" placeholder="Titulo" value="{contenido[0]}">
            </label>
            <br>
            <label for="descripcion">
                <h2>Descripción</h2>
                <br>
                <textarea name="descripcion" id="descripcionedit" placeholder="Descripcion">{contenido[1]}</textarea>
            </label>
            <br>
            <button id="registrar" onclick="editarsqlcontenido({contenido[2]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_contacto_edit', methods=['POST'])
def buscador_contacto_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT contacts.Facebook, contacts.Instagram, contacts.Tik_tok, contacts.Email, contacts.Twitter, contacts.Whatsapp, contacts.Phone, contacts.Id_contact FROM contacts WHERE contacts.Id_contact=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
                <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>
                Editar Contactos
            </h1>
            <br>
            <div id="formulario_contactos">
                <div id="izquierda">
                    <label for="Facebook">
                        <h2>
                            Facebook
                        </h2>
                        <br>
                        <input type="text" id="Facebookd" placeholder="Facebook" value="{contenido[0]}">
                    </label>
                    <br>
                    <label for="Instagram">
                        <h2>
                            Instagram
                        </h2>
                        <br>
                        <input type="text" id="Instagramd" placeholder="Instagram" value="{contenido[1]}">
                    </label>
                    <br>
                    <label for="Tik_Tok">
                        <h2>
                            Tik Tok
                        </h2>
                        <br>
                        <input type="text" id="Tik_Tokd" placeholder="Tik Tok" value="{contenido[2]}">
                    </label>
                    <br>
                    <label for="Email">
                        <h2>
                            Email
                        </h2>
                        <br>
                        <input type="text" id="Emaild" placeholder="Email" value="{contenido[3]}">
                    </label>
                </div>
                <div id="derecha">
                    <label for="Twiter">
                        <h2>
                            Twitter
                        </h2>
                        <br>
                        <input type="text" id="Twiterd" placeholder="Twitter" value="{contenido[4]}">
                    </label>
                    <br>
                    <label for="Whatsapp">
                        <h2>
                            Whatsapp
                        </h2>
                        <br>
                        <input type="text" id="Whatsappd" placeholder="Whatsapp" value="{contenido[5]}">
                    </label>
                    <br>
                    <label for="Telefono">
                        <h2>
                            Telefono
                        </h2>
                        <br>
                        <input type="text" id="Telefonod" placeholder="Telefono" value="{contenido[6]}">
                    </label>
                </div>
            </div>
            <br>
            <button id="registrar" onclick="actualizartabalcontactos({contenido[7]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/buscador_season_edit', methods=['POST'])
def buscador_season_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT season_specification.season, season_specification.Id_season FROM season_specification WHERE season_specification.Id_season=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <div class="alinear">
                <h1>
                    Edición de temporada
                </h1>
                <br>
                <label for="temporada">
                    <h2>
                        Temporada
                    </h2>
                    <br>
                    <input type="text" id="temporadad" placeholder="Temporada" value="{contenido[0]}">
                </label>
                <br>
                <button id="registrar" onclick="editarsqltemporada({contenido[1]})">Actualizar</button>
            </div>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_season_delete', methods=['POST'])
def buscador_season_delete():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta para obtener la temporada actual
            sql_query = """
                SELECT season_specification.season, season_specification.Id_season 
                FROM season_specification 
                WHERE season_specification.Id_season = :id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            # Consulta para obtener todas las temporadas
            sql_all = """
                SELECT season_specification.Id_season, season_specification.season 
                FROM season_specification;
            """
            temporadas = connection.execute(text(sql_all)).fetchall()

            # Construcción del HTML
            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <div class="alinear">
                <h1>Eliminación de temporada</h1>
                <br>
                <h2>Selecciona una temporada para remplazar la temporada a los productos</h2>
                <select id="temporadaeli">
            """
            for info in temporadas:
                if id_contenido != info[0]:  # Excluir la temporada actual
                    html += f'<option value="{info[0]}">{info[1]}</option>'

            html += f"""
                </select>
                <br>
                <button id="registrar" onclick="eliminarProducto({contenido[1]})">Eliminar</button>
            </div>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404: Algo salió mal en la consulta", mimetype='text/html')

@app.route('/api/buscador_users_delete', methods=['POST'])
def buscador_users_delete():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    if not id_contenido:
        return Response("ID no proporcionado", mimetype='text/html', status=400)

    try:
        init_db()
        with engine.connect() as connection:
            # Consulta para obtener otros administradores
            sql_query = """
                SELECT users.Id_user, users.User 
                FROM users 
                WHERE users.Rol = "administrador" AND users.Id_user != :id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchall()

            # Verificar si hay otros administradores
            if not contenido:
                return Response(
                    "No se encontró otro administrador para heredar los productos",
                    mimetype='text/html',
                    status=400
                )

            # Construcción del HTML
            html = """
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <div class="alinear">
                <h1>Eliminación de Usuarios</h1>
                <br>
                <h2>Selecciona otro administrador para reasignar los productos:</h2>
                <select id="administradorEli">
            """
            for admin in contenido:
                html += f'<option value="{admin.Id_user}">{admin.User}</option>'

            html += f"""
                </select>
                <br>
                <button id="registrar" onclick="eliminarProducto({id_contenido})">Actualizar</button>
            </div>
            """

            return Response(html, mimetype='text/html', status=200)

    except Exception as e:
        app.logger.error(f"Error en la consulta: {e}")
        return Response("Error interno del servidor", mimetype='text/html', status=500)

@app.route('/api/buscador_comentario_edit', methods=['POST'])
def buscador_comentario_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT comments.Punctuation, comments.Comment, comments.Id_coment FROM comments WHERE comments.Id_coment=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <div class="alinear">
                <h1>
                    Edición de Comentario
                </h1>
                <br>
                <label for="califad">
                    <h2>
                        Comentario
                    </h2>
                    <br>
                    <input type="number" id="califad" placeholder="Calificación" value="{contenido[0]}">
                </label>
                <label for="comentariod">
                    <h2>
                        Comentario
                    </h2>
                    <br>
                    <textarea id="comentariod" placeholder="Comentario">{contenido[1]}</textarea>
                </label>
                <br>
                <button id="registrar" onclick="editarsqlcomentario({contenido[2]})">Actualizar</button>
            </div>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
      
@app.route('/api/buscador_users_edit', methods=['POST'])
def buscador_users_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Estado, users.Id_user FROM users WHERE users.Id_user=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Datos del usuario</h1>
            <h2>Usuario</h2>
            <p>{contenido[0]}</p>
            <br>
            <h2>Email</h2>
            <p>{contenido[1]}</p>
            <br>
            <h2>Nombre</h2>
            <p>{contenido[2]}</p>
            <br>
            <h2>Apellido paterno</h2>
            <p>{contenido[3]}</p>
            <br>
            <h2>Apellido materno</h2>
            <p>{contenido[4]}</p>
            <br>
            """
            if contenido[5]=="administrador":
                html+=f"""
                    <h2 for="estado">Rol</h2>
                    <select id="rol" name="rol">
                        <option value="administrador" selected>Administrador</option>
                        <option value="cliente">Cliente</option>
                    </select>
                    <br>
                """
            else:
                html+=f"""
                    <h2 for="estado">Rol:</h2>
                    <select id="rol" name="rol">
                        <option value="administrador">Administrador</option>
                        <option value="cliente" selected>Cliente</option>
                    </select>
                    <br>
                """
            if contenido[6]=="Activo":
                html+=f"""
                    <h2 for="estado">Estado:</h2>
                    <select id="estado" name="estado">
                        <option value="Activo" selected>Activo</option>
                        <option value="Inactivo">Inactivo</option>
                    </select>
                    <br>
                """
            else:
                html+=f"""
                    <h2 for="estado">Estado:</h2>
                    <select id="estado" name="estado">
                        <option value="Activo">Activo</option>
                        <option value="Inactivo" selected>Inactivo</option>
                    </select>
                    <br>
                """
            html+=f"""
            <br>
            <button id="registrar" onclick="editarsqlcontenido({contenido[7]})">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_users_edit_solo', methods=['POST'])
def buscador_users_edit_solo():
    informacion = request.get_json()
    id_contenido = session['id_usuario']

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname FROM users WHERE users.Id_user=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Datos del usuario</h1>
            <h2>Usuario</h2>
            <input type="text" name="" id="usuariod" value="{contenido[0]}">
            <br>
            <h2>Email</h2>
            <input type="text" name="" id="emaild" value="{contenido[1]}">
            <br>
            <h2>Nombre</h2>
            <input type="text" name="" id="nombred" value="{contenido[2]}">
            <br>
            <h2>Apellido paterno</h2>
            <input type="text" name="" id="apellidopaternod" value="{contenido[3]}">
            <br>
            <h2>Apellido materno</h2>
            <input type="text" name="" id="apellidomaternod" value="{contenido[4]}">
            <br>
            <h2>Nueva contraseña</h2>
            <input type="password" name="" id="contraseñanuevad">
            <br>
            <h2>Contraseña anterior</h2>
            <input type="password" name="" id="contraseñaanteriord">
            <br>
            <button id="registrar" onclick="editarsqlcontenidousuariosolo()">Actualizar</button>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
    
@app.route('/api/buscador_producto_edit', methods=['POST'])
def buscador_producto_edit():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Material_composition, products.Model, products.FK_id_season, products.Size, products.Name, products.Description, products.Price_per_unit, products.Color, products.url_imagen, users.User, products.Id_product FROM products INNER JOIN users ON products.FK_Id_user=users.Id_user WHERE products.Id_product=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            direccion_imagen= url_for('static', filename=f'image/imagenes_productos/{contenido[8]}', _external=True)
            
            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Edición de producto</h1>

            <div class="izquierda">
                <img src="{direccion_imagen}" alt="{contenido[8]}" style="width:300px;height:auto;">
                <br>
                <label for="modelo">Modelo:{contenido[1]}
                </label>
                <br>
                """
            with engine.connect() as connection:
                result = connection.execute(text('SELECT season_specification.Id_season, season_specification.season FROM season_specification;'))
                temporadas = result.fetchall()
                html += f"""
                <select id="temporadad">
                    """
                for info in temporadas:
                    if contenido[2]==info[0]:
                        html += f"""
                            <option value="{info[0]}" selected>{info[1]}</option>
                        """
                    else:
                        html += f"""
                            <option value="{info[0]}">{info[1]}</option>
                        """
                html += f"""
                    </select>
                """
            html +=f"""
                <br>
                <label for="tamaño">Tamaño:
                    <input type="text" name="tamaño" id="tamañod" value="{contenido[3]}">
                </label>
                <br>
                <label for="nombre">Nombre:
                    <input type="text" name="nombre" id="nombred" value="{contenido[4]}">
                </label>
                <br>
            </div>

            <div class="derecha">
                <label for="descripcion">Descripción:
                    <textarea name="descripcion" id="descripciond">{contenido[5]}</textarea>
                </label>
                <br>
                <label for="precio_lot">Precio (lote):
                    <input type="number" name="precio_lot" id="precio_lotd" value="{contenido[6]}">
                </label>
                <br>
                <label for="color">Color:
                    <input type="text" name="color" id="colord" value="{contenido[7]}">
                </label>
                <br>
                <label for="materia">Material de composición:
                    <input type="text" name="materia" id="materiad" value="{contenido[0]}">
                </label>
                <br>
            </div>

            <br>
            <button id="registrar" onclick="editarsqlcontenido({contenido[10]})">Editar</button>
            """

            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

#Solisitar datos para pantalla de detalles
@app.route('/api/buscador_producto_dettalles', methods=['POST'])
def buscador_producto_dettalles():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT products.Material_composition, products.Model, season_specification.season, products.Size, products.Name, products.Description, products.Price_per_unit, products.Color, products.url_imagen, users.User FROM products INNER JOIN season_specification ON products.FK_id_season=season_specification.Id_season INNER JOIN users ON products.FK_Id_user=users.Id_user WHERE products.Id_product=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            direccion_imagen= url_for('static', filename=f'image/imagenes_productos/{contenido[8]}', _external=True)
            
            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Detalles de producto</h1>

            <h2>Imagen</h2>
            <img src="{direccion_imagen}" alt="{contenido[8]}" style="width:300px;height:auto;">

            <h2>Modelo</h2>
            <p>{contenido[1]}</p>

            <h2>Temporada</h2>
            <p>{contenido[2]}</p>

            <h2>Tamaño</h2>
            <p>{contenido[3]}</p>

            <h2>Nombre</h2>
            <p>{contenido[4]}</p>

            <h2>Descripción</h2>
            <p>{contenido[5]}</p>

            <h2>Precio por unidad</h2>
            <p>${contenido[6]}</p>

            <h2>Color</h2>
            <p>{contenido[7]}</p>

            <h2>Composición del material</h2>
            <p>{contenido[0]}</p>

            <h2>Usuario que lo registro</h2>
            <p>{contenido[9]}</p>
            """
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')

@app.route('/api/buscador_users_detalles', methods=['POST'])
def buscador_users_detalles():
    informacion = request.get_json()
    id_contenido = informacion.get('id')

    try:
        init_db()
        with engine.connect() as connection:
            sql_query = """
                SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname, users.Rol, users.Estado, users.Id_user FROM users WHERE users.Id_user=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_contenido})
            contenido = result.fetchone()

            if contenido is None:
                return Response("No se encontró contenido", mimetype='text/html')

            html = f"""
            <span class="cerrar" onclick="cerrarModal()">&times;</span>
            <h1>Datos del usuario</h1>
            <h2>Usuario</h2>
            <p>{contenido[0]}</p>
            <br>
            <h2>Email</h2>
            <p>{contenido[1]}</p>
            <br>
            <h2>Nombre</h2>
            <p>{contenido[2]}</p>
            <br>
            <h2>Apellido paterno</h2>
            <p>{contenido[3]}</p>
            <br>
            <h2>Apellido materno</h2>
            <p>{contenido[4]}</p>
            <br>
            <h2>Rol</h2>
            <p>{contenido[5]}</p>
            <br>
            <h2>Estado</h2>
            <p>{contenido[6]}</p>   
            <br>
            """
            
            return Response(html, mimetype='text/html')
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return Response("Error 404", mimetype='text/html')
    
#Actualizar datos
@app.route('/actualizar_contenido', methods=['POST'])
def actualizar_contenido():
    init_db()

    data = request.get_json()
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    id = data.get('id')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_check = """
            SELECT 1 
            FROM content 
            WHERE content.Title = :titulo
            AND content.Id_contenido != :id;
            """
            result = connection.execute(text(sql_check), {
                "titulo": titulo,
                "id":id
            }).fetchone()
            
            if result:
                return jsonify({"message": "Título ya registrado, favor de cambiarlo"}), 400
            
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `content` SET `Title` = :titulo, `Describe` = :descripcion WHERE `content`.`Id_contenido` = :id;
            """
            print(f"Ejecutando consulta: {sql_query}")

            # Ejecutar la consulta
            connection.execute(text(sql_query), {
                "titulo": titulo,
                "descripcion": descripcion,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@app.route('/actualizar_contacto', methods=['POST'])
def actualizar_contacto():
    init_db()

    data = request.get_json()
    facebook = data.get('facebook')
    instagram = data.get('instagram')
    tik_tok = data.get('tik_tok')
    email = data.get('email')
    twitter = data.get('twitter')
    whatsapp = data.get('whatsapp')
    phone = data.get('phone')
    id = data.get('id_contact')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `contacts` 
                SET `Facebook` = :facebook, 
                    `Instagram` = :instagram, 
                    `Tik_tok` = :tik_tok, 
                    `Email` = :email, 
                    `Twitter` = :twitter, 
                    `Whatsapp` = :whatsapp, 
                    `Phone` = :phone 
                WHERE `contacts`.`Id_contact` = :id;
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "facebook": facebook,
                "instagram": instagram,
                "tik_tok": tik_tok,
                "email": email,
                "twitter": twitter,
                "whatsapp": whatsapp,
                "phone": phone,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

@app.route('/actualizar_temporada', methods=['POST'])
def actualizar_temporada():
    init_db()

    data = request.get_json()
    season = data.get('season')
    id = data.get('id')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))

            sql_query = """
                UPDATE `season_specification` SET `season_specification`.`season` = :season WHERE `season_specification`.`Id_season` = :id;
            """

            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "season": season,
                "id":id
            })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

@app.route('/actualizar_comentario', methods=['POST'])
def actualizar_comentario():
    init_db()

    informacion = request.get_json()
    comentario = informacion.get('comentario')
    calif = informacion.get('calif')
    id_comentario = informacion.get('id_comentario')

    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga

    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                SELECT comments.FK_Id_customer
                FROM comments
                WHERE  comments.Id_coment=:id;
            """
            result = connection.execute(text(sql_query), {"id": id_comentario})
            contenido = result.fetchone()
            if contenido[0] == session['id_usuario']:
                # Iniciar una transacción
                connection.execute(text("START TRANSACTION;"))

                sql_query = """
                    UPDATE `comments` SET `Punctuation` = :calif, `Comment` = :comentario WHERE `comments`.`Id_coment` = :id_comentario;
                """

                # Ejecutar la consulta con los datos
                connection.execute(text(sql_query), {
                    "calif": calif,
                    "comentario":comentario,
                    "id_comentario":id_comentario
                })

                # Finalizar transacción
                connection.execute(text("COMMIT;"))
            else:
                return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500
        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500
    
@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    init_db()

    # Captura los datos del formulario
    temporada = request.form.get('temporada')
    tamaño = request.form.get('tamaño')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio_lot = request.form.get('precio_lot')
    color = request.form.get('color')
    materia = request.form.get('materia')
    producto_id = request.form.get('id')

    try:
        # Abrir una nueva conexión para actualizar el producto
        with engine.connect() as connection:
            # Iniciar transacción
            connection.execute(text("START TRANSACTION;"))

            # Consulta SQL para actualizar el producto
            sql_query = """
            UPDATE `products` 
            SET 
                `Material_composition` = :materia,
                `FK_id_season` = :temporada,
                `Size` = :tamaño,
                `Name` = :nombre,
                `Description` = :descripcion,
                `Price_per_unit` = :precio_lot,
                `Color` = :color,
                `FK_Id_user` = :user_id
            WHERE `Id_product` = :producto_id;
            """

            # Ejecutar la consulta de actualización
            connection.execute(text(sql_query), {
                "materia": materia,
                "temporada": temporada,
                "tamaño": tamaño,
                "nombre": nombre,
                "descripcion": descripcion,
                "precio_lot": precio_lot,
                "color": color,
                "user_id": session['id_usuario'],
                "producto_id": producto_id
            })
            ###########################
            # Confirmar transacción
            connection.execute(text("COMMIT;"))

        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores
        return jsonify({"message": f"Error al actualizar el producto: {str(e)}"}), 500

@app.route('/actualizar_usuario_solito', methods=['POST'])
def actualizar_usuario_solito():
    init_db()

    usuario = request.form.get('usuario')
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    apellidop = request.form.get('apellidop')
    apellidom = request.form.get('apellidom')
    contraseñanueva = request.form.get('contraseñanueva')
    contraseñaanterior = request.form.get('contraseñaanterior')
    
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga
    
    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                SELECT users.Password FROM users WHERE users.Id_user=:id;
            """
            result = connection.execute(text(sql_query), {"id": session['id_usuario']})
            contenido = result.fetchone()
            
            if not check_password_hash(contenido[0], contraseñaanterior):
                return jsonify({"message": "Contraseña incorrecta"}), 400
            
            # Iniciar una transacción
            connection.execute(text("START TRANSACTION;"))
            
            if not contraseñanueva:
                sql_query = """
                    UPDATE `users` SET `User` = :usuario, `Email` = :correo, `Name` = :nombre, `Surname` = :apellidopaterno, `Lastname` = :apellidomaterno WHERE `users`.`Id_user` = :id_usuario;
                """
                # Ejecutar la consulta con los datos
                connection.execute(text(sql_query), {
                    "usuario": usuario,
                    "correo":email,
                    "nombre":nombre,
                    "apellidopaterno":apellidop,
                    "apellidomaterno":apellidom,
                    "id_usuario": session['id_usuario'],
                })
            else:
                contraseñanueva = generate_password_hash(contraseñanueva, method='pbkdf2:sha256', salt_length=16)
                
                sql_query = """
                    UPDATE `users` SET `User` = :usuario, `Password` = :contraseñanueva, `Email` = :correo, `Name` = :nombre, `Surname` = :apellidopaterno, `Lastname` = :apellidomaterno WHERE `users`.`Id_user` = :id_usuario;
                """
                # Ejecutar la consulta con los datos
                connection.execute(text(sql_query), {
                    "usuario": usuario,
                    "contraseñanueva":contraseñanueva,
                    "correo":email,
                    "nombre":nombre,
                    "apellidopaterno":apellidop,
                    "apellidomaterno":apellidom,
                    "id_usuario": session['id_usuario'],
                })

            # Finalizar transacción
            connection.execute(text("COMMIT;"))
            
        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

@app.route('/actualizar_user', methods=['POST'])
def actualizar_user():
    init_db()

    data = request.get_json()

    # Extraer los valores del JSON
    rol = data.get('rol')
    estado = data.get('estado')
    id = data.get('id')
    #time.sleep(5)  #Espera 5 segundos para testear pantalla de carga
    
    # Intento de insertar datos
    try:
        with engine.connect() as connection:
            sql_query = """
                        UPDATE `users` SET `Rol` = :rol, `Estado` = :estado WHERE `users`.`Id_user` = :id_usuario;
                """
            # Ejecutar la consulta con los datos
            connection.execute(text(sql_query), {
                "rol":rol,
                "estado":estado,
                "id_usuario": id,
            })
            connection.execute(text("COMMIT;"))
        return jsonify({"message": "Actualizacion exitosa"}), 200
    except Exception as e:
        # Hacer rollback en caso de error
        with engine.connect() as connection:
            connection.execute(text("ROLLBACK;"))

        # Manejo de errores (nimodillo)
        return jsonify({"message": f"Error al actualizar: {str(e)}"}), 500

#inicio de secion y cerrar seción
@app.route('/login', methods=['POST'])
def login():
    init_db()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    #time.sleep(3)
    try:
        with engine.connect() as connection:
            sql_query = """
            SELECT users.Password FROM users WHERE users.Email=:email;
            """
            result = connection.execute(text(sql_query), {
                "email": email,
            }).fetchone()
            if not result:
                 return jsonify({"message": "Usuario o contraseña incorrectos"})
            
            if not check_password_hash(result[0], password):
                return jsonify({"message": "Usuario o contraseña incorrectos"})
            
            sql_query = """
            SELECT users.Rol, users.Id_user, users.Name, users.Estado FROM users WHERE users.Email=:email;
            """
            result = connection.execute(text(sql_query), {
                "email": email
            }).fetchone()
            
            if not result[3]=="Inactivo":
                session['inicio_cesion'] = True
                
                if result:
                    #Almacenar los datos del usuario
                    session['permiso_usuario'] = result[0]
                    session['id_usuario'] = result[1]
                    session['usuario_usuario'] = result[2]
                    
                    if session['permiso_usuario']=="administrador":
                        session['permiso_admin'] = True
                        
                    # Redirige según el rol
                    if session['permiso_usuario'] == 'administrador':
                        return jsonify({"redirect": "/administrador"})
                    else:
                        return jsonify({"redirect": "/"})
                else:
                    return jsonify({"message": "Usuario o contraseña incorrectos"})
            else:
                return jsonify({"message": "Error en el servidor"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()

    session['inicio_cesion'] = False
    session['permiso_admin'] = False
    # Redirigir a la página de inicio o a donde desees
    return jsonify({"redirect": "/"}) # Redirige a la página principal

#Direccionamientos####################################################################
@app.route('/')
def home():
    return render_template('index.html', inicio=session['inicio_cesion'], admin=session['permiso_admin'])

def login_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'permiso_usuario' not in session or session['permiso_usuario'] != role:
                return redirect(url_for('home'))  # Redirigir al inicio si no está autenticado
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/administrador_productos')
@login_required('administrador')
def administrador_productos():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT season_specification.Id_season, season_specification.season FROM season_specification;'))
        temporadas = result.fetchall()
        html = f"""
        <select id="temporada">
            """
        for info in temporadas:
            html += f"""
                <option value="{info[0]}">{info[1]}</option>
                """
        html += f"""
        </select>
        """
    response = make_response(render_template('administracion.html', temporada_form=html))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_season')
@login_required('administrador')
def administrador_season():
    response = make_response(render_template('administracion_season.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_contact')
@login_required('administrador')
def administrador_contact():
    response = make_response(render_template('administracion_contactos.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_content')
@login_required('administrador')
def administrador_content():
    response = make_response(render_template('administracion_content.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador_user')
@login_required('administrador')
def administrador_user():
    response = make_response(render_template('administracion_users.html'))
    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/administrador')
@login_required('administrador')
def administrador():
    #Cantidad de productos
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener el conteo de productos
            sql_query = """
                SELECT COUNT(*) AS total_productos FROM products;
            """
            result = connection.execute(text(sql_query))
            contenido = result.fetchone()  # Recupera la fila de resultados

        # Extraer el conteo desde el resultado (accediendo por índice)
        total_productos = contenido[0] if contenido else 0
    except Exception as e:
        app.logger.error(f"Error al obtener el total de productos: {e}")
        total_productos = "Error al obtener datos"

    #Cantidad de clientes
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener el conteo de productos
            sql_query = """
                SELECT COUNT(*) FROM users WHERE users.Rol="cliente";
            """
            result = connection.execute(text(sql_query))
            contenido = result.fetchone()  # Recupera la fila de resultados

        # Extraer el conteo desde el resultado (accediendo por índice)
        total_clientes = contenido[0] if contenido else 0
    except Exception as e:
        app.logger.error(f"Error al obtener el total de productos: {e}")
        total_clientes = "Error al obtener datos"
    
    #Ultimo producto registrado
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener el conteo de productos
            sql_query = """
                SELECT products.Name FROM products WHERE products.Id_product = ( SELECT MAX(products.Id_product) FROM products );
            """
            result = connection.execute(text(sql_query))
            contenido = result.fetchone()  # Recupera la fila de resultados

        # Extraer el conteo desde el resultado (accediendo por índice)
        ultimo_producto_registrado = contenido[0] if contenido else 0
    except Exception as e:
        app.logger.error(f"Error al obtener el total de productos: {e}")
        ultimo_producto_registrado = "Error al obtener datos"
    
    #Ultimo comentario registrado
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener el conteo de productos
            sql_query = """
                SELECT comments.Punctuation, comments.Comment, products.Name, products.Id_product FROM comments INNER JOIN products ON comments.FK_Id_product=products.Id_product WHERE comments.Id_coment = ( SELECT MAX(comments.Id_coment) FROM comments );
            """
            result = connection.execute(text(sql_query))
            contenido = result.fetchone()  # Recupera la fila de resultados

        # Extraer el conteo desde el resultado (accediendo por índice)
        ultimo_comentario_registrado = contenido if contenido else "No hay comentarios"
    except Exception as e:
        app.logger.error(f"Error al obtener el total de productos: {e}")
        ultimo_comentario_registrado = "Error al obtener datos"
        
    #Producto mejor calificado
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener el conteo de productos
            sql_query = """
                SELECT 
                    products.Name, products.Id_product, products.url_imagen, 
                    AVG(comments.Punctuation) AS AvgPunctuation
                FROM 
                    products
                INNER JOIN 
                    comments ON comments.FK_Id_product = products.Id_product
                GROUP BY 
                    products.Name;
            """
            result = connection.execute(text(sql_query))
            contenido = result.fetchone()  # Recupera la fila de resultados

        # Extraer el conteo desde el resultado (accediendo por índice)
        producto_mejor_calificado = contenido if contenido else "No hay comentarios"
    except Exception as e:
        app.logger.error(f"Error al obtener el total de productos: {e}")
        producto_mejor_calificado = "Error al obtener datos"
    
    # Datos de la gráfica
    try:
        with engine.connect() as connection:
            # Consulta SQL para obtener la cantidad de comentarios por puntuación (1-5)
            sql_query = """
                SELECT 
                    comments.Punctuation, 
                    COUNT(*) AS NumComments
                FROM 
                    comments
                WHERE 
                    comments.Punctuation BETWEEN 1 AND 5  -- Asegura que las puntuaciones sean entre 1 y 5
                GROUP BY 
                    comments.Punctuation
            """
            result = connection.execute(text(sql_query))
            datos_grafica = result.fetchall()  # Recupera todas las filas de resultados

            # Crear listas para las puntuaciones y la cantidad de comentarios
            puntuaciones = [1, 2, 3, 4, 5]
            conteo_comentarios = [0] * 5  # Inicializa una lista con 0 para cada puntuación (1-5)

            # Depuración: Imprimir los datos obtenidos
            for row in datos_grafica:
                print(f"Puntuación: {row[0]}, Número de Comentarios: {row[1]}")

            # Llenar el conteo de comentarios con los datos obtenidos
            for row in datos_grafica:
                puntuacion = int(row[0])  # Asegurarse de que puntuacion sea un entero
                num_comentarios = row[1]
                conteo_comentarios[puntuacion - 1] = num_comentarios  # Ajuste porque las puntuaciones empiezan en 1

            # Verificar el contenido de conteo_comentarios después de llenarlo
            print(f"Conteo de comentarios: {conteo_comentarios}")

    except Exception as e:
        app.logger.error(f"Error al obtener los datos: {e}")
        puntuaciones = [1, 2, 3, 4, 5]
        conteo_comentarios = [0, 0, 0, 0, 0]

    # Crear la respuesta del renderizado con la variable de conteo
    response = make_response(render_template(
        'administracion_inicio.html',
        total_productos=total_productos,
        total_clientes=total_clientes,
        ultimo_producto_registrado=ultimo_producto_registrado,
        ultimo_comentario_registrado=ultimo_comentario_registrado,
        producto_mejor_calificado=producto_mejor_calificado,

        puntuaciones=puntuaciones,
        conteo_comentarios=conteo_comentarios,  # Agregamos el conteo de comentarios
    ))


    # Control de caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

#######################################################################################################################
@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', inicio=session['inicio_cesion'], admin=session['permiso_admin'])

@app.route('/producto', methods=['GET'])
def producto():
    id_producto = request.args.get('id')
    with engine.connect() as connection:
        sql_query = """
                    SELECT products.Material_composition, products.Model, season_specification.season, products.Size, products.Name, products.Description, products.Price_per_unit, products.Color, products.url_imagen, users.User, products.Id_product FROM products INNER JOIN season_specification ON products.FK_id_season=season_specification.Id_season INNER JOIN users ON products.FK_Id_user=users.Id_user WHERE products.Id_product=:id;
                """
        result = connection.execute(text(sql_query), {"id": id_producto})
        contenido = result.fetchone()
    #print(sesion_activa)
    return render_template('producto.html',cont=contenido, inicio=session['inicio_cesion'], admin=session['permiso_admin'])

@app.before_request
def inicializar_variable():
    if 'inicio_cesion' not in session:
        session['inicio_cesion'] = False
        
    if 'permiso_admin' not in session:
        session['permiso_admin'] = False
    
    if 'id_usuario' not in session:
        session['id_usuario'] = None
        
    if 'usuario_usuario' not in session:
        session['usuario_usuario'] = None

@app.route('/cuenta_usuario', methods=['GET','POST'])
def cuenta_usuario():
    with engine.connect() as connection:
        sql_query = """
                    SELECT users.User, users.Email, users.Name, users.Surname, users.Lastname FROM users WHERE users.Id_user=:id;
                """
        result = connection.execute(text(sql_query), {"id":session['id_usuario']})
        contenido = result.fetchone()
    #print(sesion_activa)
    return render_template('usuario_administra.html',cont=contenido, inicio=session['inicio_cesion'], admin=session['permiso_admin'])

################################################################################################################################
@app.route('/inicio_usuario')
def inicio_usuario():
    return render_template('registro_Inicio.html')

@app.route('/inicio_sesion')
def iniciar_sesion():
    checkbox_checked = True
    return render_template('registro_Inicio.html', checkbox_checked=checkbox_checked)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', inicio=session['inicio_cesion'], admin=session['permiso_admin']), 404

# Inicio del servidor
if __name__ == '__main__':
    init_db()
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
