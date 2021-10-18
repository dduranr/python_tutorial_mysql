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
#   g                   Es un objecto especial que es único para cada petición. Es usado para almacenar datos que pueden ser accedidos desde múltiples funciones durante la petición. La conexión es almacenada y reusada en vez de crear una nueva conexión.


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
# from flaskr.db import get_db
from flaskr.paquetes.backend.formularios.auth import AuthFormLogin
import functools
import bcrypt
import sys

# Importamos los modelos a usar
from flaskr.paquetes.backend.modelos.user import *

bp = Blueprint('auth', __name__, url_prefix='/auth')



# session es un dict que almacena datos entre solicitudes. Cuando la validación tiene éxito, el ID de usuario se almacena en una nueva sesión. Los datos se almacenan en una cookie que se envía al navegador y, a continuación, el navegador los devuelve con las solicitudes posteriores. Flask firma los datos de forma segura para que no puedan ser manipulados.



# RUTAS
# RUTAS
# RUTAS
@bp.route('/login', methods=['GET'])
def login():
    try:
        if 'user_id' in session:
            return redirect(url_for('backend.auth.welcome'))
        else:
            formulario = AuthFormLogin()
            return render_template('backend/auth/login.html', formulario=formulario)

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
            formulario = AuthFormLogin()
            if formulario.validate_on_submit():
                email = request.form['email']
                contrasena = request.form['contrasena']
                contrasena_encode = contrasena.encode('utf-8')

                usuario = User.getByEmail(email)

                if usuario:
                    bd_contrasena = usuario.contrasena
                    bd_contrasena = bd_contrasena.encode('utf-8')

                    # Si en la BD se guarda un texto cualquiera y no un hash (p.e. abc), el navegador devuelve: ValueError: Invalid salt
                    if(bcrypt.checkpw(contrasena_encode, bd_contrasena)):
                        session.clear()
                        session['user_id'] = usuario.id
                        session['user_nombre'] = usuario.nombre
                        session['user_email'] = usuario.email
                        return redirect(url_for('backend.auth.welcome'))
                    else:
                        flash('Usuario/contraseña incorrectos', 'danger')
                        return redirect(url_for('backend.auth.login'))
                else :
                    flash('Usuario/contraseña incorrectos', 'danger')
                    return redirect(url_for('backend.auth.login'))
            else:
                flash('Imposible crear sesión. Algún dato es incorrecto', 'danger')
                return redirect(url_for('backend.auth.login'))

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



@bp.route('/welcome', methods=['GET'])
def welcome():
    try:
        if request.method == 'GET':
            return render_template('backend/auth/welcome.html')

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



# Al comienzo de cada solicitud (en toda la app), si un usuario está logueado, su información debe cargarse y ponerse a disposición de cualquier vista.
# bp.before_app_request() registra una función que se ejecuta antes que la función de visualización, sin importar qué URL se solicite. load_logged_in_user comprueba si una identificación de usuario está almacenada en la session y obtiene los datos de ese usuario de la base de datos, almacenándolos en g.user, lo que dura la duración de la solicitud. Si no hay una identificación de usuario, o si la identificación no existe, g.user valdrá None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()

        g.user = User.getById(user_id)



# Para cerrar la sesión, debe eliminar la identificación de usuario del archivo session. Entonces load_logged_in_user no cargará un usuario en solicitudes posteriores.
@bp.route('/logout', methods=['GET'])
def logout():
    try:
        if request.method == 'GET':
            session.clear()
            return redirect(url_for('index'))

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)






# Requerir autenticación en otras vistas
# Crear, editar y eliminar publicaciones de blog requerirá que un usuario inicie sesión. Se puede usar un decorador para verificar esto para cada vista a la que se aplica.
# Este decorador devuelve una nueva función de vista que envuelve la vista original a la que se aplica. La nueva función comprueba si un usuario está cargado y, de lo contrario, redirige a la página de inicio de sesión. Si se carga un usuario, se llama a la vista original y continúa normalmente. Utilizará este decorador al escribir las vistas del blog.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('backend.auth.login'))

        return view(**kwargs)

    return wrapped_view
