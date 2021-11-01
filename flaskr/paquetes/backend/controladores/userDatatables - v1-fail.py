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
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr import create_app
from flaskr.paquetes.backend.formularios.user import UserFormCreate
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flaskr.paquetes.backend.modelos.user import *
import functools
import bcrypt
import sys
import os




bp = Blueprint('userDatatables', __name__, url_prefix='/userDatatables')


# RUTAS
# RUTAS
# RUTAS
@bp.route('/datatable')
def datatable():

    # Importar la instancia app devuelta por esta función, dentro de los módulos en su proyecto es propenso a problemas de importación circular. Al usar el patrón de "fábrica de aplicaciones" no habrá una instancia app para importar en absoluto. Flask resuelve este problema con el contexto de la aplicación. En lugar de referirse a la instancia "app" directamente, usa el proxy "current_app", que apunta a la aplicación que maneja la actividad actual. Si intenta acceder a current_app, o cualquier cosa que lo use, fuera del contexto de la aplicación, obtendrá este mensaje de error: RuntimeError: Working outside of application context. Si ve este error puede enviar un contexto manualmente ya que tiene acceso directo al archivo app. Úselo en un bloque "with" junto con app_context(), y todo lo que se ejecute en el bloque tendrá acceso current_app.
    # Estas 3 lineas sirven para tener acceso a la aplicación, no directamente con el objeto app, sino mediante el contexto de la aplicación, como en Java
    flaskr = create_app()
    flaskr.app_context().push()
    db = SQLAlchemy(flaskr)


    query = User.getAll()
    # query = User.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.nombre.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total_filtered = User.queryCount()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_nombre = request.args.get(f'columns[{col_index}][data]')
        if col_nombre not in ['nombre', 'email']:
            col_nombre = 'nombre'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_nombre)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        # query = query.order_by(*order)
        query = User.queryOrderBy(order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.queryCount(),
        'draw': request.args.get('draw', type=int),
    }
