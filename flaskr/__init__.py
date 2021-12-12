# Este archivo __init__.py tiene un doble propósito: contiene la "application factory" y le dice a Python que la carpeta "flaskr" debería tratarse como un paquete. Es decir, cualquier carpeta que contenga un __init__.py será tratada como un paquete.

import os
from os import environ
# from os import environ, path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging, logging.config
from datetime import datetime
from flaskr.paquetes.general.constantes import Constantes

# create_app() es la función de "application factory"
def create_app(test_config=None):
	# instance_relative_config le dice a la app que los archivos de configuración son relativos a la carpeta de instancia (instance). Ésta esta ubicada fuera del paquete "flaskr" y puede almacenar datos que no deberían entrar en el sistema de control de versiones, tales como key secrets y archivos de BD. El archivo de configuraciones .flaskenv automáticamente es leído si se ubica en la raíz del proyecto (por lo cual no es necesario declarar sus variables en app.config).
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = environ.get('SECRET_KEY'),
        # DATABASE es la ruta donde se guarda el archivo de BD SQLite. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder. You’ll learn more about the database in the next section.
        # DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI'),
        RECAPTCHA_PUBLIC_KEY = environ.get('RECAPTCHA_PUBLIC_KEY'),
        RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY'),
    )


    FOLDER_ROOT = environ.get('FOLDER_ROOT')
    FOLDER_LOGS = environ.get('FOLDER_LOGS')

    logging.config.fileConfig(FOLDER_ROOT+'\\log.ini')
    logger = logging.getLogger('MainLogger')

    fh = logging.FileHandler(FOLDER_LOGS+'\\{:%Y%m%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(filename)s (%(lineno)04d): %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.debug('ERste es el debug message')
    logger.info('ERste es el info message')
    logger.warn('ERste es el warn message')
    logger.error('ERste es el error message')
    logger.critical('ERste es el critical message')









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

    """
        Finalmente hacemos que este función "application factory" devuelva la app.
        Cómo recuperar la instancia "app"
            Documentación:
                https://flask.palletsprojects.com/en/1.1.x/appcontext/#the-application-context
                https://flask.palletsprojects.com/en/1.1.x/api/#flask.current_app
            Al usar el patrón de fábrica de aplicaciones (como lo hago aquí) no habrá en absoluto una instancia "app" para importar. Así que olvidar siquiera intentar esto:
                from flaskr import app
            Flask resuelve este problema con el contexto de la aplicación. En lugar de referirse directamente a una "app", usa el proxy "current_app", que apunta a la aplicación que maneja la actividad actual.

            Si intenta acceder a current_app, o cualquier cosa que lo use, fuera del contexto de una aplicación, obtendrá este mensaje de error:
                RuntimeError: Working outside of application context.
            Si ve ese error, puede enviar un contexto manualmente ya que tiene acceso directo al archivo app. Use app_context() en un bloque "with", y todo lo que se ejecute en el bloque tendrá acceso current_app.

            Ejemplo de recuperar "app"
                Aquí en __init__.py
                    1. Afuera del create_app()
                        db = SQLAlchemy()
                    2. Dentro del create_app()
                        with app.app_context():
                            db = SQLAlchemy(app)

                En el módulo externo
                    from flaskr import db, create_app
                    def delete(id):
                        db.create_all(app=create_app())
                        db.session.query(MiModelo).filter_by(id=id).delete()
                        db.session.commit()

    """
    return app
