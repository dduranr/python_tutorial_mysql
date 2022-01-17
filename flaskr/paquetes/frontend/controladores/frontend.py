from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.general.constantes import Constantes
from flaskr.paquetes.backend.modelos.blog import *
from flaskr import mail

bp = Blueprint('frontend', __name__)
logger = fileLogSystem()



# Esta ruta se encarga de mostrar la home
@bp.route('/')
def index():
    return render_template('frontend/home/index.html')



# Esta ruta se encarga de mostrar a) la vista principal del blog y b) la vista full de un blogspot
@bp.route('/blog', defaults={'id': None})
@bp.route('/blog/<id>')
def blog(id):
    try:

        # SIGO AQUÍ
        # SIGO AQUÍ
        # SIGO AQUÍ
        #           1. Crear sección de contacto en el front
        #           2. Sacar este envío de correo de aquí y ponerlo en el controlador de la sección de contacto cuando alguien haga submit en el formulario de contacto

        msg = Message(
            subject    = "¡Flask Email funciona!",
            sender     = "no.more.hegel@gmail.com",
            recipients = ["official.dduran@gmail.com"],
            body       = "¡Este es una prueba de email que envío con Gmail and Python!",
            html       = '<p>Perfecto, <strong>esto es HTML dentro del correo</strong></p>'
        )
        mail.send(msg)


        if id is None:
            page = int(request.args.get('page', 1)) # Si no llega este param, por defecto page será igual a 1
            post_pagination = Blog.all_paginated(page, Constantes.ITEMS_PER_PAGE)
            return render_template('frontend/blog/index.html', post_pagination=post_pagination)
        else:
            post = Blog.getById(id)
            return render_template('frontend/blog/full.html', post=post)

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.error(error)
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
