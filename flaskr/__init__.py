# Este archivo __init__.py tiene un doble propósito: contiene la "application factory" y le dice a Python que la carpeta "flaskr" debería tratarse como un paquete. Es decir, cualquier carpeta que contenga un __init__.py será tratada como un paquete.

import os
from os import environ
from flask import Flask

# create_app() es la función de "application factory"
def create_app(test_config=None):
	# instance_relative_config le dice a la app que los archivos de configuración son relativos a la carpeta de instancia (instance). Ésta esta ubicada fuera del paquete "flaskr" y puede almacenar datos que no deberían entrar en el sistema de control de versiones, tales como key secrets y archivos de BD. El archivo de configuraciones .flaskenv automáticamente es leído si se ubica en la raíz del proyecto (por lo cual no es necesario declarar sus variables en app.config).
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = environ.get('SECRET_KEY'),
        # DATABASE es la ruta donde se guarda el archivo de BD SQLite. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder. You’ll learn more about the database in the next section.
        # DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    )

    # xxx = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    # print('xxx: ', xxx)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py')
        pass
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # Flask no crea automáticamente un "instance folder", pero necesita crearse porque el proyecto guardará ahí el archivo de BD SQLite
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Esto sirve para llamar la BD SQLite
    # from . import db
    # db.init_app(app)


    # Recuperamos los archivos blueprints
    from . paquetes.frontend.controladores import frontend
    from . paquetes.backend.controladores import backend
    from . paquetes.backend.controladores import auth
    from . paquetes.backend.controladores import user
    from . paquetes.backend.controladores import datatables
    from . paquetes.backend.controladores import blog

    # Anidamos los blueprints del back al blueprint "backend" para que así todas las urls del back tengan como prefijo "backend"
    backend.bp.register_blueprint(auth.bp)
    backend.bp.register_blueprint(user.bp)
    backend.bp.register_blueprint(datatables.bp)
    backend.bp.register_blueprint(blog.bp)

    # Registramos los blueprints del back y front
    app.register_blueprint(frontend.bp)
    app.register_blueprint(backend.bp)

    # La siguiente línea asocia el endpoint 'index' con la URL raíz (/). Así que url_for('index') o url_for('blog.index') harán lo mismo, generando la misma URL de cualquier manera.
    app.add_url_rule('/', endpoint='index')





    # Finalmente hacemos que este función "application factory" devuelva la app.
    # IMPORTANTE. Puesto que las variables de configuración son variables de entorno, así presisamente podrán ser recuperadas en cualquier otro lugar de la app:
    #       import os
    #       SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # Hasta donde sé, no es posible recuperar la variable app, digamos así:
    #       from ....__init__ import create_app
    #       create_app.app
    return app
