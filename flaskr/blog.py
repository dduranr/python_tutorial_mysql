from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)



# RUTAS
# RUTAS
# RUTAS
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)




@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')




# Tanto las vistas update y delete tendrán que buscar un post por ID y comprobar si el autor coincide con el usuario conectado. Para evitar la duplicación de código, puede escribir una función para obtener post y llamarla desde cada vista.
# abort() generará una excepción especial que devuelve un código de estado HTTP. Se necesita un mensaje opcional para mostrar el error; de lo contrario, se usa un mensaje predeterminado. 404significa "No encontrado" y 403significa "Prohibido". ( 401significa "No autorizado", pero redirige a la página de inicio de sesión en lugar de devolver ese estado).

# El check_authorargumento se define para que la función se pueda usar para obtener un postsin verificar el autor. Esto sería útil si escribiera una vista para mostrar una publicación individual en una página, donde el usuario no importa porque no está modificando la publicación.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post





# A diferencia de las vistas que has escrito hasta ahora, la función update toma un argumento ID. Eso corresponde a <int:id>. Se verá asi: /1/update. Flask capturará el 1, se asegurará de que sea un int y lo pasará como argumento ID. Si no especifica int, y en su lugar escribes <id>, se traducirá como cadena. Para generar una URL para la página de actualización, url_for() necesita el ID.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)




@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))




