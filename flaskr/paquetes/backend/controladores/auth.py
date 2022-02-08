from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Markup
)
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flaskr.paquetes.backend.formularios.auth import *
from flaskr.paquetes.backend.modelos.user import *
from flaskr.paquetes.general.helpers import *
from flaskr import login_manager
from sqlalchemy import exc
import functools
import bcrypt
import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = fileLogSystem()



# Esta ruta se encarga de mostrar formulario para hacer login
@bp.route('/login', methods=['GET'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('backend.auth.welcome'))
        else:
            formulario = AuthFormLogin()
            return render_template('backend/auth/login.html', formulario=formulario)

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



# Esta ruta se encarga de mostrar formulario para hacer login
@bp.route('/forbidden', methods=['GET'])
def forbidden():
    try:
        return render_template('backend/auth/forbidden.html')
        # return redirect(url_for('backend.auth.forbidden'))

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



# Esta ruta se encarga de iniciar sesión
@bp.route('/store', methods=['POST'])
def store():
    try:
        if request.method == 'POST':
            errores = ''
            formulario = AuthFormLogin()
            if formulario.validate_on_submit():
                email = request.form['email']
                contrasena = request.form['contrasena']
                contrasena_encode = contrasena.encode('utf-8')

                usuario = User.getByEmail(formulario.email.data)

                if usuario and usuario.check_password(password=formulario.contrasena.data):
                    # login_user(usuario, remember=formulario.remember_me.data)

                    login_user(usuario)

                    next_page = request.args.get('next')

                    # DOCUMENTAR ESTO
                    # DOCUMENTAR ESTO
                    # DOCUMENTAR ESTO
                    #                   Ya encontré por qué "current_user is not being persisted between requests"
                    #                   Justo cuando hacía login, current.is_authenticated devuelve TRUE, pero justo inmediatamente al hacer redirect a WELCOME, ya valía FALSE. Esto era porque yo estaba limpiando las variables de sesión:

                    # session.clear()
                    # session['user_id'] = usuario.id
                    # session['user_nombre'] = usuario.nombre
                    # session['user_email'] = usuario.email

                    # Como la info del usuario actualmente logueado está en current_user, al parecer no tengo necesidad de generar esas variables de sesión

                    # SIGO CON
                    # SIGO CON
                    # SIGO CON
                    #       Primero poner el menú, que desapareció porque ya no están disponibles las variables de sesión, y en su lugar (ahí en el header), usar current_user.
                    #       Quitar las funciones que use cada vez que hago
                    #           from flask_login import LoginManager, login_user, logout_user, login_required, current_user
                    #       Después documentar bien cómo se usar Flask-Login



                    print('---------------------> FROM auth::store is_authenticated')
                    print(current_user.is_authenticated)

                    print('---------------------> FROM auth::store is_active')
                    print(current_user.is_active)

                    print('---------------------> FROM auth::store is_anonymous')
                    print(current_user.is_anonymous)

                    print('---------------------> FROM auth::store get_id')
                    print(current_user.get_id)
                    print('')
                    print('')
                    print('')


                    return redirect(next_page or url_for('backend.auth.welcome'))
                else :
                    errores += 'Usuario/contraseña incorrecto'
            else:
                errores += 'Imposible crear sesión: '

            flash(Markup('Imposible loguearse: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('backend.auth.login'))

    except exc.SQLAlchemyError as e:
        error = ''
        if "2002" in str(e):
            error = 'Al parecer la base de datos está caída.'
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



# Esta ruta se encarga de mostrar vista de bienvenida en caso de logueo satisfactorio
@bp.route('/welcome', methods=['GET'])
def welcome():

    print('---------------------> FROM welcome::login is_authenticated')
    print(current_user.is_authenticated)

    print('---------------------> FROM welcome::login is_active')
    print(current_user.is_active)

    print('---------------------> FROM welcome::login is_anonymous')
    print(current_user.is_anonymous)

    print('---------------------> FROM welcome::login get_id')
    print(current_user.get_id)

    try:
        if request.method == 'GET':
            return render_template('backend/auth/welcome.html')

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



# Al comienzo de cada solicitud (en toda la app), si un usuario está logueado, su información debe cargarse y ponerse a disposición de cualquier vista.
# bp.before_app_request() registra una función que se ejecuta antes que la función de visualización, sin importar qué URL se solicite. load_logged_in_user comprueba si una identificación de usuario está almacenada en la session y obtiene los datos de ese usuario de la base de datos, almacenándolos en g.user, lo que dura la duración de la solicitud. Si no hay una identificación de usuario, o si la identificación no existe, g.user valdrá None.
@bp.before_app_request
def load_logged_in_user():
    try:
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = User.getById(user_id)

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



# Esta ruta se encarga de cerrar la sesión
@bp.route('/logout', methods=['GET'])
def logout():
    try:
        if request.method == 'GET':
            # logout_user()
            session.clear()
            return redirect(url_for('index'))

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



@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.getById(user_id)
    return None



# Por último, tenemos la unauthorizedruta, que utiliza el unauthorized_handlerdecorador para tratar con usuarios no autorizados. Cada vez que un usuario intente acceder a nuestra aplicación y no esté autorizado, esta ruta se activará.
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('backend.auth.forbidden'))



# Esta función se encarga de requerir autenticación para cualquier ruta en donde se indique
# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('backend.auth.login'))

#         return view(**kwargs)

#     return wrapped_view
