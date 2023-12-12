from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app = Flask(__name__)


# Set the uploads folder configuration
app.config['CARPETA'] = os.path.join(os.getcwd(), 'uploads')

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema_empleados'

mysql.init_app(app)

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')
def index():
    # Obtener todos los empleados al cargar la página
    empleados = get_empleados_from_db()
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/destroy/<int:id>')
def destroy(id):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Obtener el nombre de la foto del empleado antes de eliminarlo
        cursor.execute("SELECT foto FROM sistema_empleados WHERE id=%s", (id,))
        foto_a_eliminar = cursor.fetchone()[0]

        # Eliminar al empleado
        cursor.execute("DELETE FROM sistema_empleados WHERE id=%s", (id,))
        conn.commit()

        # Eliminar la foto correspondiente al empleado
        if foto_a_eliminar:
            foto_path = os.path.join("uploads", foto_a_eliminar)
            os.remove(foto_path)

    except Exception as e:
        return str(e)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Obtener los detalles del empleado para la edición
        cursor.execute("SELECT * FROM sistema_empleados WHERE id=%s", (id,))
        empleado_tuple = cursor.fetchone()

        # Convertir la tupla a un diccionario PARA SU USO CORRECTO
        empleado = {
            'id': empleado_tuple[0],
            'nombre': empleado_tuple[1],
            'email': empleado_tuple[2],
            'foto': empleado_tuple[3]
        }

        # Obtener la URL completa de la foto actual
        foto_actual_url = url_for('uploads', nombreFoto=empleado['foto'])

    except Exception as e:
        return str(e)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    return render_template('empleados/edit.html', empleado_a_editar=empleado, foto_actual_url=foto_actual_url)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Obtener valores del formulario
        nombre = request.form.get('txtNombre')
        email = request.form.get('txtCorreo')
        foto = request.files.get('txtFoto')

        # Obtener el nombre de la foto actual del empleado
        cursor.execute("SELECT foto FROM sistema_empleados WHERE id=%s", (id,))
        foto_actual = cursor.fetchone()[0]

        # Actualizar la base de datos
        if foto.filename != '':
            # Si se proporciona una nueva foto, guardarla y actualizar la referencia en la base de datos
            now = datetime.now()
            tiempo = now.strftime("%Y%H%M%S")
            nuevoNombreFoto = tiempo + foto.filename
            foto.save(os.path.join("uploads", nuevoNombreFoto))

            # Eliminar la foto actual del empleado
            if foto_actual:
                foto_path_actual = os.path.join("uploads", foto_actual)
                os.remove(foto_path_actual)

            # Actualizar el registro en la base de datos con la nueva información
            sql = "UPDATE sistema_empleados SET nombre=%s, email=%s, foto=%s WHERE id=%s;"
            datos = (nombre, email, nuevoNombreFoto, id)
        else:
            # Si no se proporciona una nueva foto, eliminar todos los empleados y redirigir a la página principal
            cursor.execute("DELETE FROM sistema_empleados;")
            conn.commit()
            return redirect('/')

        cursor.execute(sql, datos)
        conn.commit()

    except Exception as e:
        return str(e)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    return redirect('/')

@app.route('/store', methods=['POST'])
def storage():
    try:
        # Obtener valores del formulario
        nombre = request.form.get('txtNombre')
        email = request.form.get('txtCorreo')
        foto = request.files.get('txtFoto')

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        if foto.filename != '':
            nuevoNombreFoto = tiempo + foto.filename
            foto.save(os.path.join("uploads", nuevoNombreFoto))

        # Validar que 'nombre' no esté vacío o sea None
        if not nombre:
            raise ValueError("El campo 'nombre' no puede ser nulo o estar vacío.")

        # Realizar la inserción en la base de datos
        sql = "INSERT INTO `sistema_empleados` (`nombre`, `email`, `foto`) VALUES (%s, %s, %s);"
        datos = (nombre, email, nuevoNombreFoto)

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()

        # Obtener todos los empleados después de la inserción
        empleados = get_empleados_from_db()

    except Exception as e:
        return str(e)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

    # Renderizar la plantilla con la lista actualizada de empleados
    return redirect('/')

# Función para obtener todos los empleados de la base de datos
def get_empleados_from_db():
    try:
        sql = "SELECT * FROM `sistema_empleados`;"
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(sql)
        empleados = cursor.fetchall()

        # Crear una lista de diccionarios para representar los resultados
        empleados_list = [{'id': emp[0], 'nombre': emp[1], 'email': emp[2], 'foto': emp[3]} for emp in empleados]

        return empleados_list

    except Exception as e:
        return str(e)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)





