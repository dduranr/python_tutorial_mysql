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
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.paquetes.backend.formularios.user import UserFormCreate
from flaskr.paquetes.backend.modelos.user import User
from flaskr.paquetes.backend.formularios.user import *
from flaskr.paquetes.general.constantes import Constantes
from sqlalchemy import exc
from datetime import datetime
import functools
import bcrypt
import sys

bp = Blueprint('user', __name__, url_prefix='/user')
# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()



# RUTAS
# RUTAS
# RUTAS
@bp.route('/index', methods=['GET'])
def index():
    # try:
    return render_template('backend/user/index.html')

    # except exc.SQLAlchemyError as e:
    #     # En teoría si se devuelve el siguiente error, la cosa se soluciona con un sessionDB.rollback().
    #     if 't reconnect until invalid transaction is rolled back' in str(e):
    #         print('Existe error reconnect')

    #     error = "Excepción SQLAlchemyError: " + str(e)
    #     return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    # except TypeError as e:
    #     error = "Excepción TypeError: " + str(e)
    #     return render_template('backend/errores/error.html', error="TypeError: "+error)
    # except ValueError as e:
    #     error = "Excepción ValueError: " + str(e)
    #     return render_template('backend/errores/error.html', error="ValueError: "+error)
    # except Exception as e:
    #     error = "[1] Excepción general: " + str(e.__class__)
    #     return render_template('backend/errores/error.html', error=error)



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
        error = "[2] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/store', methods=['POST'])
def store():
    try:
        if request.method == 'POST':
            error = ''
            formulario = UserFormCreate()
            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y-%m-%d %H:%M:%S")

                nombre = request.form['nombre']
                email = request.form['email']
                contrasena = request.form['contrasena']
                contrasena_encode = contrasena.encode('utf-8')
                contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)

                userExistente = User.getByEmail(email)

                if userExistente:
                    error = error + 'Imposible crear usuario, pues '+email+' ya existe como usuario en base de datos'
                else :
                    usuario = User(nombre=nombre, email=email, contrasena=contrasena_crypt)
                    usuario.post()
                    flash('Usuario agregado', 'success')
                    return redirect(url_for('backend.user.index'))
            else:
                error = error+'Imposible crear usuario. Algún dato es incorrecto. (Recuerda que: '+Constantes.REQUISITOS_CONTRASENA+')'

            if len(error)>0:
                flash(error, 'danger')
            return redirect(url_for('backend.user.create'))

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
        error = "[3] Excepción general: " + str(e.__class__)
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
        error = "[4] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/update/<id>', methods=['POST'])
def update(id):
    try:
        error = ''
        user = User.getById(id)
        if (request.method == 'POST'):
            formulario = UserFormUpdate()
            if formulario.validate_on_submit():
                nombre = request.form['nombre']
                email = request.form['email']
                contrasena = request.form['contrasena']

                userExistente = User.getById(id)

                if not userExistente:
                    error = error + 'Imposible actualizar user, pues el ID '+id+' no existe más en base de datos'
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
                error = error+'Imposible actualizar usuario. Algún dato es incorrecto. (Recuerda que: '+Constantes.REQUISITOS_CONTRASENA+')'

            if len(error)>0:
                flash(error, 'danger')
                return redirect(url_for('backend.user.edit',id=id))

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
        error = "[5] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



@bp.route('/delete/<id>', methods=['POST'])
def delete(id):
    try:
        if (request.method == 'POST'):
            respuesta = {
                'estatus': False,
                'toastrMsg': '...',
                'toastrType': 'danger',
                'toastrTitle': '...'
            }
            userExistente = User.getById(id)
            userNombre = '?'
            booleano = bool(userExistente)

            if booleano:
                userNombre = userExistente.nombre
                User.delete(id)
                respuesta = {
                    'estatus': True,
                    'toastrMsg': 'Usuario eliminado ('+userNombre+' con ID: '+id+')',
                    'toastrType': 'success',
                    'toastrTitle': '¡Yeeeha!'
                }
            else:
                respuesta = {
                    'estatus': False,
                    'toastrMsg': 'Imposible eliminar user, pues no se pudo recuperar el usuario (ID: '+id+') de la base de datos',
                    'toastrType': 'danger',
                    'toastrTitle': '¡Ooops!'
                }

            return jsonify(respuesta)

    except exc.SQLAlchemyError as e:
        error = ''
        if "1451" in str(e):
            error = 'Al parecer este usuario está asignado a otro elemento (¿como autor de un blogpost?). Por tanto, antes de intentar eliminarlo deberás borrar todos los elementos a los que está asignado, o si no borrarlos, al menos sí reasignarlos a otro usuario.'
        else:
            error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "[6] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)
