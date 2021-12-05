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
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Markup
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.paquetes.backend.controladores.auth import login_required
from flaskr.paquetes.backend.formularios.blog import *
from flaskr.paquetes.backend.modelos.blog import *
from flaskr.paquetes.general.helpers import *
from sqlalchemy import exc
from datetime import datetime


# from flask import request
from werkzeug.datastructures import CombinedMultiDict

bp = Blueprint('blog', __name__, url_prefix='/blog')
INSTANCE_PATH = os.getenv('INSTANCE_PATH')



# Esta ruta se encarga de mostrar la vista index (listado de registros)
@bp.route('/index', methods=['GET'])
@login_required
def index():
    try:
        return render_template('backend/blog/index.html')

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



# Esta ruta se encarga de mostrar la vista para crear registro
@bp.route('/create', methods=['GET'])
@login_required
def create():
    # try:
    # tipo = type(INSTANCE_PATH).__name__
    # print('---------')
    # print(tipo)
    # print(INSTANCE_PATH)
    # print('---------')
    print('INSTANCE_PATH::: ', INSTANCE_PATH)

    formulario = BlogFormCreate()
    return render_template('backend/blog/create.html', formulario=formulario)

    # except TypeError as e:
    #     error = "Excepción TypeError: " + str(e)
    #     return render_template('backend/errores/error.html', error="TypeError: "+error)
    # except ValueError as e:
    #     error = "Excepción ValueError: " + str(e)
    #     return render_template('backend/errores/error.html', error="ValueError: "+error)
    # except Exception as e:
    #     error = "Excepción general: " + str(e.__class__)
    #     return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de crear registro en BD
@bp.route('/store', methods=['POST'])
@login_required
def store():
    try:
        if request.method == 'POST':

            user_id = g.user.id
            formulario = BlogFormCreate()

            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y%m%d%H%M%S")

                title = request.form['title']
                contenido = request.form['contenido']

                img = formulario.img.data
                filename = secure_filename(img.filename)
                img.save(os.path.join(
                    INSTANCE_PATH, 'img', ahora+'_'+filename
                ))

                error = None

                if not title:
                    error = 'El título es obligatorio.'
                elif not contenido:
                    error = 'El contenido es obligatorio.'

                if error is not None:
                    flash(error, 'danger')
                    return redirect(url_for('backend.blog.create'))
                else:
                    blogpost = Blog(author_id=user_id, title=title, contenido=contenido, img=filename)
                    blogpost.post()
                    flash('Post agregado', 'success')
                    return redirect(url_for('backend.blog.create'))
            else:
                flash(Markup('Imposible crear post: '+getErrorsFromWTF(formulario.errors)), 'danger')
                return redirect(url_for('backend.blog.create'))

    except exc.SQLAlchemyError as e:
        error = ''
        if "1406" in str(e):
            error = 'Al parecer el nombre del archivo es demasiado largo. Por favor intenta con un nombre más corto.'
        else:
            error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar vista para editar registro
@bp.route('/edit/<id>', methods=['GET'])
@login_required
def edit(id):
    try:
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

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de actualizar registro en BD
@bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    try:
        error = ''
        post = User.getById(id)
        if (request.method == 'POST'):
            formulario = BlogFormEdit()
            if formulario.validate_on_submit():
                author_id = request.form['author_id']
                title = request.form['title']
                contenido = request.form['contenido']

                postExistente = Blog.getById(id)

                if not postExistente:
                    error = error + 'Imposible actualizar post, pues el ID '+id+' no existe más en base de datos'
                else :
                    dataToSave = {"author_id": author_id, "title": title, "contenido": contenido}
                    Blog.put(id, dataToSave)

                    flash('Post actualizado', 'success')
                    return redirect(url_for('backend.blog.index'))
            else:
                error = error+'Imposible actualizar post. Algún dato es incorrecto.'

            if len(error)>0:
                flash(error, 'danger')
                return redirect(url_for('backend.blog.edit',id=id))

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
        error = "[5] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



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
                blogpostTitle = blogpostExistente.title
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
            error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "[6] Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)
