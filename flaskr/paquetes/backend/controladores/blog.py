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
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.paquetes.backend.controladores.auth import login_required
from flaskr.paquetes.backend.formularios.blog import BlogFormCreate
from flaskr.paquetes.backend.modelos.blog import *
from sqlalchemy import exc

bp = Blueprint('blog', __name__, url_prefix='/blog')



# RUTAS
# RUTAS
# RUTAS
@bp.route('/index', methods=['GET'])
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



@bp.route('/create', methods=['GET'])
def create():
    try:
        formulario = BlogFormCreate()
        return render_template('backend/blog/create.html', formulario=formulario)

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
@login_required
def store():
    try:
        if request.method == 'POST':
            formulario = AuthFormLogin()
            if formulario.validate_on_submit():
                title = request.form['title']
                contenido = request.form['contenido']
                error = None

                if not title:
                    error = 'El título es obligatorio.'
                elif not contenido:
                    error = 'El contenido es obligatorio.'

                if error is not None:
                    flash(error, 'danger')
                    return redirect(url_for('backend.blog.create'))
                else:
                    blogpost = Blog(author_id=g.user['id'], title=title, contenido=contenido)
                    blogpost.post()
                    flash('Post agregado', 'success')
                    return redirect(url_for('backend.blog.create'))
            else:
                flash('Imposible crear post. Algún dato es incorrecto', 'danger')
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



@bp.route('/edit', methods=['GET'])
def edit():
    try:
        formulario = BlogFormCreate()
        return render_template('backend/blog/edit.html', formulario=formulario)

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('backend/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('backend/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('backend/errores/error.html', error=error)



# A diferencia de las vistas que has escrito hasta ahora, la función update toma un argumento ID. Eso corresponde a <int:id>. Se verá asi: /1/update. Flask capturará el 1, se asegurará de que sea un int y lo pasará como argumento ID. Si no especifica int, y en su lugar escribes <id>, se traducirá como cadena. Para generar una URL para la página de actualización, url_for() necesita el ID.
@bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    blogpost = getPost(id)

    if request.method == 'POST':
        title = request.form['title']
        contenido = request.form['contenido']
        error = None

        if not title:
            error = 'El título es obligatorio.'
        elif not contenido:
            error = 'El contenido es obligatorio.'

        if error is not None:
            flash(error, 'danger')
            return redirect(url_for('backend.blog.create'))
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, contenido = ?'
                ' WHERE id = ?',
                (title, contenido, id)
            )
            db.commit()
            return redirect(url_for('backend.blog.index'))

    return render_template('blog/update.html', post=blogpost)




@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    getPost(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('backend.blog.index'))




# La siguiente función no está asignada a una ruta. Es simplemente una función que sirve internamente dentro de este controlador.
# Tanto las vistas update y delete tendrán que buscar un post por ID y comprobar si el autor coincide con el usuario conectado. Para evitar la duplicación de código, se escribe esta función que obtiene el post a actualizar o eliminar.
#   abort() genera una excepción especial que devuelve un código de estado HTTP. Se necesita un mensaje opcional para mostrar el error; de lo contrario, se usa un mensaje predeterminado.
#   El argumento check_author se define para que la función se pueda usar para obtener un post sin verificar el autor. Esto sería útil si escribiera una vista para mostrar una publicación individual en una página, donde el usuario no importa porque no está modificando la publicación.
def getPost(id, check_author=True):

    blogpost = Blog.getByAuthorId(id)

    if blogpost is None:
        abort(404, f"No existe el blogppost con id {id}.")

    if check_author and blogpost['author_id'] != g.user['id']:
        abort(403)

    return blogpost


# DOCUMENTACIÓN
#   https://www.youtube.com/watch?v=2kg_5ttL150
#   https://tutorial101.blogspot.com/2021/04/datatable-ajax-pagination-using-python.html
@bp.route('/datatable', methods=['POST'])
def datatable():
    # try:
    if request.method == 'POST':
        draw = request.form['draw']
        row = int(request.form['start'])
        rowperpage = int(request.form['length'])
        searchValue = request.form["search[value]"]
        likeString = "%" + searchValue +"%"
        # likeString = "%Volutpat%"

        print('DRAW: ', draw)
        print('ROW: ', row)
        print('ROWPERPAGE: ', rowperpage)
        print('SEARCHVALUE: ', searchValue)

        # Número total de registros sin filtrar
        totalRecords = Blog.getCountWithoutFiltering()
        print('TOTALRECORDS: ', totalRecords)
        # Número total de registros con filtro
        totalRecordwithFilter = Blog.getCountWithFiltering(likeString)
        print('TOTALRECORDWITHFILTER: ', totalRecordwithFilter)



        if searchValue=='':
            print('SE LEEEEEEEEEEEEEEEE 1')
            blogposts = Blog.getAll(row, rowperpage)
        else:
            print('SE LEEEEEEEEEEEEEEEE 2')
            blogposts = Blog.getAll2(row, rowperpage, likeString)

        print('ELEMENTOS TOTALES EN blogposts', len(blogposts))


        data = []
        if len(blogposts) > 0:
            for fila in blogposts:
                data.append({
                    'id': fila.blog.id,
                    'autor': fila.blog.author_id,
                    'autor_email': fila.user.email,
                    'titulo': fila.blog.title,
                    'editar': 'EDITAR',
                    'eliminar': 'ELIMINAR'
                })

        response = {
            'draw': draw,
            'iTotalRecords': totalRecords,
            'iTotalDisplayRecords': totalRecordwithFilter,
            'aaData': data
        }
        return jsonify(response)

    # except exc.SQLAlchemyError as e:
    #     error = "Excepción SQLAlchemyError: " + str(e)
    #     return render_template('backend/errores/error.html', error="SQLAlchemyError: "+error)
    # except TypeError as e:
    #     error = "Excepción TypeError: " + str(e)
    #     return render_template('backend/errores/error.html', error="TypeError: "+error)
    # except ValueError as e:
    #     error = "Excepción ValueError: " + str(e)
    #     return render_template('backend/errores/error.html', error="ValueError: "+error)
    # except Exception as e:
    #     error = "Excepción general: " + str(e.__class__)
    #     return render_template('backend/errores/error.html', error=error)