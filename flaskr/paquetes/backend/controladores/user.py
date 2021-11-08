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
from flaskr.paquetes.general.constantes import Constantes
from sqlalchemy import exc
from datetime import datetime
import functools
import bcrypt
import sys

bp = Blueprint('user', __name__, url_prefix='/user')
# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()


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
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



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
