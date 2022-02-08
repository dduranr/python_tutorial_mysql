# Este archivo __init__.py tiene un doble propósito: contiene la "application factory" y le dice a Python que la carpeta "flaskr" debería tratarse como un paquete. Es decir, cualquier carpeta que contenga un __init__.py será tratada como un paquete.

import os
from os import environ
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flaskr.paquetes.general.constantes import Constantes
from flaskr.paquetes.backend.modelos.user import User
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Esta línea genera un objeto BaseQuery de Flask-Sqlalchemy, no de Sqlalchemy solo. Este objeto es el que necesitaremos para usar el método paginate() en los modelos
db = SQLAlchemy()

# Para envío de correo
mail = Mail()

# Instanciamos el objeto para el uso de Flask-Login
login_manager = LoginManager()


# create_app() es la función de "application factory"
def create_app(test_config=None):
	# instance_relative_config le dice a la app que los archivos de configuración son relativos a la carpeta de instancia (instance). Ésta esta ubicada fuera del paquete "flaskr" y puede almacenar datos que no deberían entrar en el sistema de control de versiones, tales como key secrets y archivos de BD. El archivo de configuraciones .flaskenv automáticamente es leído si se ubica en la raíz del proyecto (por lo cual no es necesario declarar sus variables en app.config).
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI'),
        RECAPTCHA_PUBLIC_KEY = environ.get('RECAPTCHA_PUBLIC_KEY'),
        RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USERNAME = environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = environ.get('MAIL_PASSWORD'),
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_DEBUG = True,
    )


    # --------------------------------
    # ---   Inicializamos plugins  ---
    # --------------------------------
    # Inicializamos el objeto mail (en cualquier otro archivo puede recuperarse: from flaskr import mail)
    mail.init_app(app)

    # Flask-Login
    # load_useres fundamental para que nuestra aplicación funcione: antes de que se cargue cada página, nuestra aplicación debe verificar si el usuario está conectado o no (o si sigue conectado después de que haya transcurrido el tiempo). user_loadercarga a los usuarios por su ID único. Si se devuelve un usuario, esto significa que se ha desconectado del usuario. De lo contrario, cuando Nonese devuelve, se cierra la sesión del usuario.
    login_manager.init_app(app)


    # @login_manager.user_loader
    # def load_user(user_id):
    #     if user_id is not None:
    #         return User.getById(user_id)
    #     return None

    # # Por último, tenemos la unauthorizedruta, que utiliza el unauthorized_handlerdecorador para tratar con usuarios no autorizados. Cada vez que un usuario intente acceder a nuestra aplicación y no esté autorizado, esta ruta se activará.
    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     """Redirect unauthorized users to Login page."""
    #     return redirect(url_for('backend.auth.forbidden'))


    # Todo lo que esté dentro del WITH estará disponible en toda la app (por ejempo: from flaskr import db)
    with app.app_context():

        db = SQLAlchemy(app)

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
        from . paquetes.backend.controladores import contacto

        # Anidamos los blueprints del back al blueprint "backend" para que así todas las urls del back tengan como prefijo "backend"
        backend.bp.register_blueprint(auth.bp)
        backend.bp.register_blueprint(user.bp)
        backend.bp.register_blueprint(datatables.bp)
        backend.bp.register_blueprint(blog.bp)
        backend.bp.register_blueprint(contacto.bp)

        # Registramos los blueprints del back y front
        app.register_blueprint(frontend.bp)
        app.register_blueprint(backend.bp)

        # La siguiente línea asocia el endpoint 'index' con la URL raíz (/). Así que url_for('index') o url_for('blog.index') harán lo mismo, generando la misma URL de cualquier manera.
        app.add_url_rule('/', endpoint='index')



        return app

