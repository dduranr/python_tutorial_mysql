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
from flaskr.db import get_db
from flaskr.formularios.user import UserFormCreate
import functools
import bcrypt
import sys

bp = Blueprint('user', __name__, url_prefix='/user')



# session es un dict que almacena datos entre solicitudes. Cuando la validación tiene éxito, el ID de usuario se almacena en una nueva sesión. Los datos se almacenan en una cookie que se envía al navegador y, a continuación, el navegador los devuelve con las solicitudes posteriores. Flask firma los datos de forma segura para que no puedan ser manipulados.



# RUTAS
# RUTAS
# RUTAS
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
    db = get_db()
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

    except db.IntegrityError:
        error = f"User {email} is already posted."
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)
