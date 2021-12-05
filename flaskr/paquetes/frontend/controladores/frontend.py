from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
# from flaskr.db import get_db
from flaskr.paquetes.backend.modelos.blog import *

bp = Blueprint('frontend', __name__)



# RUTAS
# RUTAS
# RUTAS
@bp.route('/')
def index():
    return render_template('frontend/home/index.html')

@bp.route('/blog')
def blog():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, contenido, created, author_id, email'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    posts = Blog.getAll()
    return render_template('frontend/blog/index.html', posts=posts)
