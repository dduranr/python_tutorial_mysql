from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Markup, current_app
)
from flask_login import login_required
from flaskr.paquetes.backend.modelos.contacto import *
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.backend.formularios.contacto import *
from sqlalchemy import exc
from datetime import datetime
import json
import os
from os import path

bp = Blueprint('contacto', __name__, url_prefix='/contacto')
FOLDER_STATIC = os.getenv('FOLDER_STATIC')
logger = fileLogSystem()



# Esta ruta se encarga de mostrar la vista index (listado de registros)
@bp.route('/index', methods=['GET'])
@login_required
def index():
    try:
        return render_template('backend/contacto/index.html')

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.error(error)
        logging.exception(error, exc_info=True)
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



# Esta ruta se encarga de mostrar vista para editar registro (de hecho no edita nada, sólo es para ver los registros)
@bp.route('/edit/<id>', methods=['GET'])
@login_required
def edit(id):
    try:
        submission = Contacto.getById(id)
        datos = json.loads(submission.datos)
        documento = datos['documento']

        if (request.method == 'GET'):
            # Generamos el form y le pasamos los values de cada campo (en la vista los values se ponen automáticamente)
            formulario = ContactoForm(request.form, nombre=datos['nombre'], email=datos['email'], mensaje=datos['mensaje'])

            if submission:
                return render_template('backend/contacto/edit.html', submission=submission, formulario=formulario, documento=documento)
            else :
                flash('Imposible encontrar la submission', 'danger')

            return redirect(url_for('backend.contacto.index'))

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
