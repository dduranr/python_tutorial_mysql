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
from flaskr.formularios.auth import AuthFormLogin
import functools
import bcrypt
import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')



# session es un dict que almacena datos entre solicitudes. Cuando la validación tiene éxito, el ID de usuario se almacena en una nueva sesión. Los datos se almacenan en una cookie que se envía al navegador y, a continuación, el navegador los devuelve con las solicitudes posteriores. Flask firma los datos de forma segura para que no puedan ser manipulados.



# RUTAS
# RUTAS
# RUTAS
@bp.route('/login', methods=['GET'])
def login():
    try:
        if 'user_id' in session:
            return redirect(url_for('auth.welcome'))
        else:
            formulario = AuthFormLogin()
            return render_template('back/auth/login.html', formulario=formulario)

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



@bp.route('/store', methods=['POST'])
def store():
    try:
        if request.method == 'POST':
            email = request.form['email']
            contrasena = request.form['contrasena']
            db = get_db()
            error = None

            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)
            ).fetchone()

            if user is None:
                error = 'El email es incorrecto'
            elif not check_password_hash(user['contrasena'], contrasena):
                error = 'La contraseña es incorrecta.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                session['user_nombre'] = user['nombre']
                session['user_email'] = user['email']
                return redirect(url_for('auth.welcome'))

            # Si se lee esto, es porque hubo un error y no se pudo hacer el return de success
            flash(error, 'danger')
            return redirect(url_for('auth.login'))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('back/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



@bp.route('/welcome', methods=['GET'])
def welcome():
    try:
        if request.method == 'GET':
            return render_template('back/auth/welcome.html')

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



# Al comienzo de cada solicitud (en toda la app), si un usuario está logueado, su información debe cargarse y ponerse a disposición de cualquier vista.
# bp.before_app_request() registra una función que se ejecuta antes que la función de visualización, sin importar qué URL se solicite. load_logged_in_user comprueba si una identificación de usuario está almacenada en la session y obtiene los datos de ese usuario de la base de datos, almacenándolos en g.user, lo que dura la duración de la solicitud. Si no hay una identificación de usuario, o si la identificación no existe, g.user valdrá None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



# Para cerrar la sesión, debe eliminar la identificación de usuario del archivo session. Entonces load_logged_in_user no cargará un usuario en solicitudes posteriores.
@bp.route('/logout', methods=['GET'])
def logout():
    try:
        if request.method == 'GET':
            session.clear()
            return redirect(url_for('index'))

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)






# Requerir autenticación en otras vistas
# Crear, editar y eliminar publicaciones de blog requerirá que un usuario inicie sesión. Se puede usar un decorador para verificar esto para cada vista a la que se aplica.
# Este decorador devuelve una nueva función de vista que envuelve la vista original a la que se aplica. La nueva función comprueba si un usuario está cargado y, de lo contrario, redirige a la página de inicio de sesión. Si se carga un usuario, se llama a la vista original y continúa normalmente. Utilizará este decorador al escribir las vistas del blog.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
