# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   flask_sqlalchemy    ORM para SQL
#   render_template     Permite utilizar archivos HTML
#   request             Para obtener los datos de la petición de un form
#   redirect            Para hacer redirecciones
#   url_for             Para hacer redirecciones
#   flash               Manda mensajes entre vistas
#   session             Para gestionar sesiones
#   functools
#   bcrypt              Para encriptar/desemcriptar contrasaeñas
#   sys                 Para obtener el tipo de excepción


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.paquetes.backend.formularios.user import UserFormCreate
from flaskr.paquetes.backend.modelos.user import User
from flaskr.paquetes.backend.formularios.user import *
from sqlalchemy import exc
import functools
import bcrypt
import sys

bp = Blueprint('user', __name__, url_prefix='/user')



# session es un dict que almacena datos entre solicitudes. Cuando la validación tiene éxito, el ID de usuario se almacena en una nueva sesión. Los datos se almacenan en una cookie que se envía al navegador y, a continuación, el navegador los devuelve con las solicitudes posteriores. Flask firma los datos de forma segura para que no puedan ser manipulados.



# RUTAS
# RUTAS
# RUTAS
@bp.route('/index', methods=['GET'])
def index():
    try:
        return render_template('backend/user/index.html')

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/create', methods=['GET'])
def create():
    try:
        formulario = UserFormCreate()
        return render_template('backend/user/create.html', formulario=formulario)

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/store', methods=['POST'])
def store():
    # db = get_db()
    try:
        if request.method == 'POST':

            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']
            error = None

            if not nombre:
                error = 'El nombre es obligatorio.'
            elif not email:
                error = 'El email es obligatorio.'
            elif not contrasena:
                error = 'La contraseña es obligatoria.'

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO user (nombre, email, contrasena) VALUES (?, ?, ?)",
                        (nombre, email, generate_password_hash(contrasena)),
                    )
                    db.commit()
                    return redirect(url_for("backend.auth.login"))
                except db.IntegrityError:
                    error = f"El usuario {email} ya está registrado."

            flash(error, 'danger')
            return redirect(url_for("backend.user.create"))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/edit/<id>', methods=['GET'])
def edit(id):
    try:
        user = User.getById(id)
        if (request.method == 'GET'):
            # Generamos el form y le pasamos los values de cada campo (en la vista los values se ponen automáticamente)
            formulario = UserFormUpdate(request.form, nombre=user.nombre, email=user.email)

            if user:
                return render_template('backend/user/edit.html', user=user, formulario=formulario)
            else :
                flash('Imposible encontrar al usuario', 'danger')
                return redirect(url_for('backend.user.index', user=user))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/update/<id>', methods=['POST'])
def update(id):
    # try:
    user = User.getById(id)
    if (request.method == 'POST'):
        formulario = UserFormUpdate()
        if formulario.validate_on_submit():
            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']

            userExistente = User.getById(id)

            if not userExistente:
                flash('Imposible actualizar user, pues el ID '+id+' no existe más en base de datos', 'danger')
                return redirect(url_for('backend.user.index'))
            else :
                if(len(contrasena) > 0):
                    contrasena_encode = contrasena.encode('utf-8')
                    contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)
                    dataToSave = {"nombre": nombre, "email": email, "contrasena": contrasena_crypt}
                    User.put(id, dataToSave)
                else:
                    dataToSave = {"nombre": nombre, "email": email, "contrasena": userExistente.contrasena}
                    User.put(id, dataToSave)
                    flash('Usuario actualizado', 'success')
                    return redirect(url_for('backend.user.index'))
        else:
            flash('Imposible actualizar usuario. Algún dato es incorrecto', 'danger')
            return render_template('backend/user/edit.html', user=user, formulario=formulario)

    # except exc.SQLAlchemyError as e:
    #     error = "Excepción SQLAlchemyError: " + str(e)
    #     return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    # except TypeError as e:
    #     error = "Excepción TypeError: " + str(e)
    #     return render_template('backend/errores/error.html', error="TypeError: "+error)
    # except ValueError as e:
    #     error = "Excepción ValueError: " + str(e)
    #     return render_template('backend/errores/error.html', error="ValueError: "+error)
    # except Exception as e:
    #     error = "Excepción general: " + str(e.__class__)
    #     return render_template('backend/errores/error.html', error=error)



@bp.route('/delete/<id>')
def delete(id):
    try:
        userExistente = User.getById(id)

        if not userExistente:
            flash('Imposible eliminar user, pues el ID ('+id+') no coincide con ningún user en base de datos', 'danger')
            return redirect(url_for('backend.user.index'))
        else :
            User.delete(id)

        flash('Usuario eliminado', 'success')
        return redirect(url_for('backend.user.index'))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)
