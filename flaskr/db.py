import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g es un objecto especial que es único para cada petición. Es usado para almacenar datos que pueden ser accedidos desde múltiples funciones durante la petición. La conexión es almacenada y reusada en vez de crear una nueva conexión i get_deb es llamada por segunda vez en la misma petición.

# current_appes es otro objeto especial que apunta a la aplicación Flask que maneja la solicitud. Como usó una "application factory", no hay ningún objeto de aplicación al escribir el resto de su código. get_dbse llamará cuando se haya creado la aplicación y esté manejando una solicitud, por lo que current_app se puede usar.

# sqlite3.connect() establece una conexión con el archivo al que apunta la clave DATABASE de configuración. Este archivo no tiene que existir todavía, y no existirá hasta que inicialice la base de datos más tarde.

# sqlite3.Row le dice a la conexión que devuelva filas que se comportan como diccionarios. Esto permite acceder a las columnas por su nombre.

# close_db comprueba si se creó una conexión comprobando si g.db se estableció. Si la conexión existe, está cerrada. Más abajo, le informará a su aplicación sobre la función close_db en la "application factory" para que se llame después de cada solicitud.


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)