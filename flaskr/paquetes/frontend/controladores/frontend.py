from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Markup, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.paquetes.general.helpers import *
from flaskr.paquetes.general.constantes import Constantes
from flaskr.paquetes.backend.modelos.contacto import *
from flaskr.paquetes.backend.modelos.blog import *
from flaskr.paquetes.frontend.formularios.contacto import *
from flask_mail import Message
from flaskr import mail
import os
from functools import wraps

bp = Blueprint('frontend', __name__)
FOLDER_STATIC = os.getenv('FOLDER_STATIC')
logger = fileLogSystem()


# Esta ruta se encarga de mostrar la home
@bp.route('/')
def index():
    try:
        return render_template('frontend/home/index.html')

    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar a) la vista principal del blog y b) la vista full de un blogspot
@bp.route('/blog', defaults={'id': None})
@bp.route('/blog/<id>')
def blog(id):
    try:
        if id is None:
            page = int(request.args.get('page', 1)) # Si no llega este param, por defecto page será igual a 1
            post_pagination = Blog.all_paginated(page, Constantes.ITEMS_PER_PAGE)
            return render_template('frontend/blog/index.html', post_pagination=post_pagination)
        else:
            post = Blog.getById(id)
            return render_template('frontend/blog/full.html', post=post)

    except exc.SQLAlchemyError as e:
        error = 'Excepción SQLAlchemyError ('+str(e.__class__)+'): '+str(e)
        logger.error(error)
        return render_template('backend/errores/error.html', error=error)
    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de mostrar la sección Contacto
@bp.route('/contacto')
def contacto():
    try:
        formulario = ContactoForm()
        return render_template('frontend/contacto/index.html', formulario=formulario)

    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)



# Esta ruta se encarga de gestionar las submissions del formulario de contacto
@bp.route('/submissioncontacto', methods=['POST'])
def submissioncontacto():
    try:
        if request.method == 'POST':

            errores = ''
            formulario = ContactoForm()

            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y%m%d%H%M%S")
                filenameWhitDateTime = ''

                nombre = request.form['nombre']
                email = request.form['email']
                mensaje = request.form['mensaje']
                documento = formulario.documento.data
                filename = None

                if type(documento).__name__ != 'NoneType':
                    # Guardamos el archivo cargado por el usuario
                    filename = secure_filename(documento.filename)
                    filenameWhitDateTime = ahora+'_'+filename
                    documento.save(os.path.join(FOLDER_STATIC, 'submissions', filenameWhitDateTime))

                    # Armamos el jSON de datos para la BD
                    datos = '{"nombre": "'+nombre+'", "email": "'+email+'", "mensaje": "'+mensaje+'", "documento": "'+filenameWhitDateTime+'"}'
                    htmlDocumento = filenameWhitDateTime
                else:
                    datos = '{"nombre": "'+nombre+'", "email": "'+email+'", "mensaje": "'+mensaje+'", "documento": null}'
                    htmlDocumento = 'No adjuntó documento'

                contacto = Contacto(forma='contacto', datos=datos)

                # --> Guardamos mensaje en BD
                contacto.post()

                # --> Armamos todo para el envío del mensaje administrativo por email
                msg = Message(
                    subject    = "Nuevo contacto desde el sitio web hecho con Python",
                    sender     = "no.more.hegel@gmail.com",
                    recipients = ["official.dduran@gmail.com", "official.dduran@yahoo.com"],
                )
                msg.html = render_template('general/email_body_contacto.html', nombre=nombre, email=email, mensaje=mensaje, documento=htmlDocumento)

                # --> Si el user carga archivo, lo metemos como atatchment al mensaje
                if type(documento).__name__ != 'NoneType':
                    filenameSplited = os.path.splitext(filenameWhitDateTime)
                    filename_extension = filenameSplited[1]
                    filename_mime = ''

                    if filename_extension == '.jpg' or filename_extension == '.jpeg':
                        filename_mime = 'image/jpg'
                    elif filename_extension == '.png':
                        filename_mime = 'image/png'

                    with current_app.open_resource('static/submissions/'+filenameWhitDateTime) as fp:
                        msg.attach(filenameWhitDateTime, filename_mime, fp.read())

                # --> Enviamos el email
                mail.send(msg)

                flash('El mensaje fue enviado', 'success')
                return redirect(url_for('frontend.contacto'))

            else:
                errores += 'Algún dato es incorrecto.'

            flash(Markup('Imposible crear post: '+errores+' '+getErrorsFromWTF(formulario.errors)), 'danger')
            return redirect(url_for('frontend.contacto'))

    except TypeError as e:
        error = 'Excepción TypeError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except ValueError as e:
        error = 'Excepción ValueError ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
    except Exception as e:
        error = 'Excepción general ('+str(e.__class__)+'): '+str(e)
        logger.exception(error)
        return render_template('backend/errores/error.html', error=error)
