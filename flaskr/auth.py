import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



# session es un dict que almacena datos entre solicitudes. Cuando la validación tiene éxito, el ID de usuario se almacena en una nueva sesión. Los datos se almacenan en una cookie que se envía al navegador y, a continuación, el navegador los devuelve con las solicitudes posteriores. Flask firma los datos de forma segura para que no puedan ser manipulados.



# RUTAS
# RUTAS
# RUTAS
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')




# Al comienzo de cada solicitud, si un usuario está conectado, su información debe cargarse y ponerse a disposición de otras vistas.
# bp.before_app_request() registra una función que se ejecuta antes que la función de visualización, sin importar qué URL se solicite. load_logged_in_user comprueba si una identificación de usuario está almacenada en el session y obtiene los datos de ese usuario de la base de datos, almacenándolos en g.user, lo que dura la duración de la solicitud. Si no hay una identificación de usuario, o si la identificación no existe, g.user valdrá None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()




# Para cerrar la sesión, debe eliminar la identificación de usuario del archivo session. Entonces load_logged_in_user no cargará un usuario en solicitudes posteriores.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# Requerir autenticación en otras vistas
# Crear, editar y eliminar publicaciones de blog requerirá que un usuario inicie sesión. Se puede usar un decorador para verificar esto para cada vista a la que se aplica.
# Este decorador devuelve una nueva función de vista que envuelve la vista original a la que se aplica. La nueva función comprueba si un usuario está cargado y, de lo contrario, redirige a la página de inicio de sesión. Si se carga un usuario, se llama a la vista original y continúa normalmente. Utilizará este decorador al escribir las vistas del blog.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view













