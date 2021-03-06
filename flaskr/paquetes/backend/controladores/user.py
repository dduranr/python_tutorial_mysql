from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Markup
)
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flaskr.paquetes.backend.formularios.user import UserFormCreate
from flaskr.paquetes.backend.modelos.user import User
from flaskr.paquetes.backend.formularios.user import *
from flaskr.paquetes.general.constantes import Constantes
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.general.decorators import *
from sqlalchemy import exc
from datetime import datetime
import functools
import bcrypt
import sys


bp = Blueprint('user', __name__, url_prefix='/user')
# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()
logger = fileLogSystem()



# Esta ruta se encarga de mostrar la vista index (listado de registros)
@bp.route('/index', methods=['GET'])
@login_required
def index():
    try:
        return render_template('backend/user/index.html')

    except exc.SQLAlchemyError as e:
        # En teoría si se devuelve el siguiente error, la cosa se soluciona con un sessionDB.rollback().
        if 't reconnect until invalid transaction is rolled back' in str(e):
            print('Existe error reconnect')
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar la vista para crear registro
@bp.route('/create', methods=['GET'])
@login_required
@cud_privileges_required('user')
def create():
    try:
        formulario = UserFormCreate()
        return render_template('backend/user/create.html', formulario=formulario)

    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de crear registro en BD
@bp.route('/store', methods=['POST'])
@login_required
@cud_privileges_required('user')
def store():
    try:
        if request.method == 'POST':
            errores = ''
            formulario = UserFormCreate()
            if formulario.validate_on_submit():
                userExistente = User.getByEmail(formulario.email.data)

                if userExistente:
                    errores += 'Imposible crear usuario, pues '+formulario.email.data+' ya existe como usuario en base de datos'
                else :
                    usuario = User(nombre=formulario.nombre.data, email=formulario.email.data, rol=formulario.rol.data)
                    usuario.set_password(formulario.contrasena.data)
                    usuario.post()
                    # Si existiera un formulario en el frontend donde el user se crea su propia cuenta, con la siguiente línea haríamos que se logueara automáticamente
                    # login_user(usuario)
                    flash('Usuario agregado ('+formulario.email.data+')', 'success')
                    return redirect(url_for('backend.user.index'))
            else:
                errores += 'Algún dato es incorrecto. (Recuerda que: '+Constantes.REQUISITOS_CONTRASENA+')'

            flash(Markup('Imposible crear usuario: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('backend.user.create'))

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar vista para editar registro
@bp.route('/edit/<id>', methods=['GET'])
@login_required
@cud_privileges_required('user')
def edit(id):
    try:
        user = User.getById(id)
        if (request.method == 'GET'):
            # Generamos el form y le pasamos los values de cada campo (en la vista los values se ponen automáticamente)
            formulario = UserFormUpdate(request.form, nombre=user.nombre, email=user.email, rol=user.rol)

            if user:
                return render_template('backend/user/edit.html', user=user, formulario=formulario)
            else :
                flash('Imposible encontrar al usuario', 'danger')

            return redirect(url_for('backend.user.index'))

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de actualizar registro en BD
@bp.route('/update/<id>', methods=['POST'])
@login_required
@cud_privileges_required('user')
def update(id):
    try:
        errores = ''
        if (request.method == 'POST'):
            formulario = UserFormUpdate()
            if formulario.validate_on_submit():
                userExistente = User.getById(id)

                if not userExistente:
                    errores += 'Imposible actualizar user, pues el ID '+id+' no existe más en base de datos'
                else :
                    if(len(formulario.contrasena.data) > 0):
                        dataToSave = {"nombre": formulario.nombre.data, "email": formulario.email.data, "contrasena": formulario.contrasena.data, "rol": formulario.rol.data}
                        # Hasheamos la nueva contraseña al formato tal como lo necesita Flask-Login
                        dataToSave['contrasena'] = generate_password_hash(
                            dataToSave.pop('contrasena'),
                            method='sha256'
                        )
                        User.put(id, dataToSave)
                        flash('Usuario actualizado con pass ('+str(id)+': '+userExistente.nombre+')', 'success')
                    else:
                        dataToSave = {"nombre":formulario.nombre.data, "email":formulario.email.data, "contrasena": userExistente.contrasena, "rol":formulario.rol.data}
                        User.put(id, dataToSave)
                        flash('Usuario actualizado sin pass ('+str(id)+': '+userExistente.nombre+')', 'success')
                    return redirect(url_for('backend.user.index'))
            else:
                errores += 'Algún dato es incorrecto. (Recuerda que: '+Constantes.REQUISITOS_CONTRASENA+')'

            flash(Markup('Imposible actualizar usuario: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('backend.user.edit',id=id))

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de eliminar registro en BD
@bp.route('/delete/<id>', methods=['POST'])
@login_required
@cud_privileges_required('user')
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
            error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
