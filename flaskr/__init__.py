# Este archivo __init__.py tiene un doble propósito: contiene la "application factory" y le dice a Python que la carpeta "flaskr" debería tratarse como un paquete. Es decir, cualquier carpeta que contenga un __init__.py será tratada como un paquete.

import os
from os import environ
from flask import Flask

# create_app() es la función de "application factory"
def create_app(test_config=None):
    SECRET_KEY = environ.get('SECRET_KEY')
	# instance_relative_config=True le dice a la app que los archivos de configuración son relativos a la carpeta de instancia (instance). Ésta esta ubicada fuera del paquete "flaskr" y puede almacenar datos que no deberían entrar en el sistema de control de versiones, tales como key secrets y archivos de BD. El archivo de configuraciones .flaskenv automáticamente es leído si se ubica en la raíz del proyecto.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = SECRET_KEY,
        # DATABASE es la ruta donde se guarda el archivo de BD SQLite. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder. You’ll learn more about the database in the next section.
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Flask no crea automáticamente un "instance folder", pero necesita crearse porque el proyecto guardará ahí el archivo de BD SQLite
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Esto sirve para llamar la BD
    from . import db
    db.init_app(app)


    # Registro de blueprints
    from . import auth
    from . import blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    # La siguiente línea asocia el endpoint 'index' con la URL raíz (/). Así que url_for('index') o url_for('blog.index') harán lo mismo, generando la misma URL de cualquier manera.
    app.add_url_rule('/', endpoint='index')





    # Finalmente hacemos que este función "application factory" devuelva la app
    return app
