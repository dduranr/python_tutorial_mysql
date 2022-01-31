from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Markup, current_app
)
from flaskr.paquetes.backend.controladores.auth import login_required
from flaskr.paquetes.frontend.modelos.contacto import *
from flaskr.paquetes.general.helpers import *
from sqlalchemy import exc
from datetime import datetime
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
