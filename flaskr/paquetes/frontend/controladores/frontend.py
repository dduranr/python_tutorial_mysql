from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.backend.modelos.blog import *

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
        if id is None:
            posts = Blog.getAll('created_at', False)
            # SIGO AQUÍ
            # SIGO AQUÍ
            # SIGO AQUÍ
            #           Paginación:
            #               1. Recuperar el número total de posts
            #               2. Con el número anterior, armar el paginador HTML aqui mismo
            #               3. Agregar parámetro al render_template: paginacion=paginacionHTML
            #               4. Finalmente, en la vista simplemente {{ paginacion }}
            return render_template('frontend/blog/index.html', posts=posts)
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
