from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Markup
)
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, login_required, current_user
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
                    login_user(usuario, remember=formulario.remember_me.data)

                    # login_user(usuario)

                    next_page = request.args.get('next')

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
@login_required
def welcome():
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



# Esta ruta se encarga de cerrar la sesión
@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        if request.method == 'GET':
            logout_user()
            # session.clear()
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



# Por último, tenemos la ruta unauthorized, que utiliza el decorador unauthorized_handler para tratar con usuarios no autorizados. Cada vez que un usuario intente acceder a nuestra aplicación y no esté autorizado, esta ruta se activará.
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('backend.auth.forbidden'))



# Esta ruta muestra la página PROHIBIDO que se muestra cuando un user no autenticado intenta abrir una ruta para users logueados
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
