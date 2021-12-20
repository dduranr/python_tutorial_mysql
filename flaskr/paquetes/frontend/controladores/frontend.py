from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.backend.modelos.blog import *

bp = Blueprint('frontend', __name__)
logger = fileLogSystem()



# Esta ruta se encarga de mostrar la vista principal del blog
@bp.route('/')
def index():
    return render_template('frontend/home/index.html')



@bp.route('/blog', defaults={'id': None})
@bp.route('/blog/<id>')
def blog(id):
    try:
        if id is None:
            posts = Blog.getAll()
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
