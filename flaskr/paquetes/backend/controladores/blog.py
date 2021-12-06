from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Markup, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.paquetes.backend.controladores.auth import login_required
from flaskr.paquetes.backend.formularios.blog import *
from flaskr.paquetes.backend.modelos.blog import *
from flaskr.paquetes.general.helpers import *
from sqlalchemy import exc
from datetime import datetime
import os
# import os.path
from os import environ, path
import logging, logging.config

bp = Blueprint('blog', __name__, url_prefix='/blog')
INSTANCE_PATH = os.getenv('INSTANCE_PATH')

# -------------------------------------start - LOG
log_file_path1 = 'C:\\laragon\\www\\python\\web\\flask-tutorial-mysql\\flaskr\\log.ini'

# FORMA 1. Funciona a medias, porque guarda INFOs auqnue le digas que sólo guarde a partir de ERROR
# now = datetime.now()
# hoy = now.strftime("%Y%m%d")
# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=hoy+'_log.log', filemode='a', level=logging.ERROR)

# FORMA 2
# Cómo configurar log.config: https://docs.python.org/3.3/howto/logging.html#configuring-logging
# No lanza error, pero igual no guarda nada en el log
# log_file_path2 = 'C:\\laragon\\www\\python\\web\\flask-tutorial-mysql\\flaskr\\logs.log'
# logging.config.fileConfig(log_file_path1, disable_existing_loggers=False)
# # logging.config.fileConfig(log_file_path1, defaults={'logfilename': log_file_path2})

# FORMA 3. Finalmente parece que sí sirve
# https://michaelheap.com/using-ini-config-with-python-logger/
# SIGO CON
# SIGO CON
# SIGO CON. Ver si efectivamente guarda sólo de ERROR para arriba
logging.config.fileConfig(log_file_path1)
logger = logging.getLogger('sLogger')

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

# logging.debug('[0] Esto es un DEBUG')
# logging.info('[0] Esto es un INFO')
# logging.warning('[0] Esto es un WARNING')
# logging.error('[0] Esto es un ERROR')
# logging.critical('[0] Esto es un CRITICAL')


# -------------------------------------end - LOG


# Esta ruta se encarga de mostrar la vista index (listado de registros)
@bp.route('/index', methods=['GET'])
@login_required
def index():
    try:
        return render_template('backend/blog/index.html')

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar la vista para crear registro
@bp.route('/create', methods=['GET'])
@login_required
def create():
    try:
        formulario = BlogFormCreate()
        return render_template('backend/blog/create.html', formulario=formulario)

    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de crear registro en BD
@bp.route('/store', methods=['POST'])
@login_required
def store():
    try:
        if request.method == 'POST':

            errores = ''
            user_id = g.user.id
            formulario = BlogFormCreate()

            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y%m%d%H%M%S")

                title = request.form['title']
                contenido = request.form['contenido']
                img = formulario.img.data
                filename = None

                if type(img).__name__ != 'NoneType':
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(
                        INSTANCE_PATH, 'img', ahora+'_'+filename
                    ))

                blogpost = Blog(author_id=user_id, title=title, contenido=contenido, img=filename)
                blogpost.post()
                flash('Post agregado', 'success')
                return redirect(url_for('backend.blog.index'))
            else:
                errores += 'Algún dato es incorrecto.'

            flash(Markup('Imposible crear post: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('backend.blog.create'))

    except exc.SQLAlchemyError as e:
        error = ''
        if "1406" in str(e):
            error = 'Al parecer el nombre del archivo es demasiado largo. Por favor intenta con un nombre más corto.'
        else:
            error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar vista para editar registro
@bp.route('/edit/<id>', methods=['GET'])
@login_required
def edit(id):
    # try:


    logging.debug('[1] Esto es un DEBUG')
    logging.info('[1] Esto es un INFO')
    logging.warning('[1] Esto es un WARNING')
    logging.error('[1] Esto es un ERROR')
    logging.critical('[1] Esto es un CRITICAL')

    current_app.logger.debug('[2] Esto es un DEBUG')
    current_app.logger.info('[2] Esto es un INFO')
    current_app.logger.warning('[2] Esto es un WARNING')
    current_app.logger.error('[2] Esto es un ERROR')
    current_app.logger.critical('[2] Esto es un CRITICAL')



    blogpost = Blog.getById(id)
    users = User.getAll("nombre")

    if (request.method == 'GET'):
        # Generamos el form y le pasamos los values de cada campo (en la vista los values se ponen automáticamente)
        formulario = BlogFormEdit(request.form, author_id=blogpost[1].author_id, title=blogpost[1].title, contenido=blogpost[1].contenido)

        if blogpost:
            return render_template('backend/blog/edit.html', blogpost=blogpost, formulario=formulario, users=users)
        else :
            flash('Imposible encontrar el post', 'danger')
            return redirect(url_for('backend.blog.index'))

    # except TypeError as e:
    #     error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
    #     return render_template('backend/errores/error.html', error=error)
    # except ValueError as e:
    #     error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
    #     return render_template('backend/errores/error.html', error=error)
    # except Exception as e:
    #     error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
    #     return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de actualizar registro en BD
@bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    try:
        errores = ''
        post = User.getById(id)
        if (request.method == 'POST'):
            formulario = BlogFormEdit()
            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y%m%d%H%M%S")
                author_id = request.form['author_id']
                title = request.form['title']
                contenido = request.form['contenido']
                img = formulario.img.data
                filename = None
                postExistente = Blog.getById(id)

                filename = secure_filename(img.filename)
                img.save(os.path.join(
                    INSTANCE_PATH, 'img', ahora+'_'+filename
                ))

                # if type(img).__name__ != 'NoneType':
                #     filename = secure_filename(img.filename)
                #     img.save(os.path.join(
                #         INSTANCE_PATH, 'img', ahora+'_'+filename
                #     ))

                if not postExistente:
                    errores += 'Imposible actualizar post, pues el ID '+id+' no existe'
                else :
                    dataToSave = {"author_id": author_id, "title": title, "contenido": contenido, "img": filename}
                    Blog.put(id, dataToSave)
                    flash('Post actualizado ('+str(id)+': '+postExistente[1].title+')', 'success')
                    return redirect(url_for('backend.blog.index'))
            else:
                errores += 'Algún dato es incorrecto.'

            flash(Markup('Imposible actualizar post: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('backend.blog.edit',id=id))

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        if environ.get('FLASK_DEBUG') == True:
            print('----------------------')
            print('FLASK_DEBUG = True')
            print('----------------------')
            raise
        else:
            print('----------------------')
            print('FLASK_DEBUG = False')
            print('----------------------')
            error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
            return render_template('backend/errores/error.html', error=error)

        # logger.exception('Error ')
        current_app.logger.info('Esto es un mensaje informativo via LOGGER')



# Esta ruta se encarga de eliminar registro en BD
@bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    try:
        if (request.method == 'POST'):
            respuesta = {
                'estatus': False,
                'toastrMsg': '...',
                'toastrType': 'danger',
                'toastrTitle': '...'
            }
            blogpostExistente = Blog.getById(id)
            blogpostTitle = '?'
            booleano = bool(blogpostExistente)

            if booleano:
                blogpostTitle = blogpostExistente[1].title
                Blog.delete(id)
                respuesta = {
                    'estatus': True,
                    'toastrMsg': 'Blogpost eliminado ('+blogpostTitle+' con ID: '+id+')',
                    'toastrType': 'success',
                    'toastrTitle': '¡Yeeeha!'
                }
            else:
                respuesta = {
                    'estatus': False,
                    'toastrMsg': 'Imposible eliminar blogpost, pues no se pudo recuperar el post (ID: '+id+') de la base de datos',
                    'toastrType': 'danger',
                    'toastrTitle': '¡Ooops!'
                }

            return jsonify(respuesta)

    except exc.SQLAlchemyError as e:
        error = ''
        if "1451" in str(e):
            error = 'Al parecer este blogpost está asignado a otro elemento (¿como post de un autor?). Por tanto, antes de intentar eliminarlo deberás borrar todos los elementos a los que está asignado, o si no borrarlos, al menos sí reasignarlos a otro autor.'
        else:
            error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        return render_template('backend/errores/error.html', error=error)
