# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

from flaskr.backend.serverside.serverside_table import ServerSideTable
from flaskr.backend.serverside import table_schemas

from flask import Blueprint, request, jsonify
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from datetime import datetime
import functools
import json


bp = Blueprint('userDatatables', __name__, url_prefix='/userDatatables')


@bp.route('/api/data', methods=['POST'])
def data():

    if request.method == 'POST':
        # Importar la instancia app devuelta por esta función, dentro de los módulos en su proyecto es propenso a problemas de importación circular. Al usar el patrón de "fábrica de aplicaciones" no habrá una instancia app para importar en absoluto. Flask resuelve este problema con el contexto de la aplicación. En lugar de referirse a la instancia "app" directamente, usa el proxy "current_app", que apunta a la aplicación que maneja la actividad actual. Si intenta acceder a current_app, o cualquier cosa que lo use, fuera del contexto de la aplicación, obtendrá este mensaje de error: RuntimeError: Working outside of application context. Si ve este error puede enviar un contexto manualmente ya que tiene acceso directo al archivo app. Úselo en un bloque "with" junto con app_context(), y todo lo que se ejecute en el bloque tendrá acceso current_app.
        # Estas 3 lineas sirven para tener acceso a la aplicación, no directamente con el objeto app, sino mediante el contexto de la aplicación, como en Java
        flaskr = create_app()
        flaskr.app_context().push()
        db = SQLAlchemy(flaskr)

        class Usuarios(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(64), index=True)
            age = db.Column(db.Integer, index=True)
            address = db.Column(db.String(256))
            phone = db.Column(db.String(20))
            email = db.Column(db.String(120))

            # Método que devuelve un usuario como un diccionario Python, el cual puede ser serializado a JSON
            def to_dict(self):
                return {
                    'name': self.name,
                    'age': self.age,
                    'address': self.address,
                    'phone': self.phone,
                    'email': self.email
                }

        query = Usuarios.query

        # search filter
        search = request.args.get('search[value]')
        if search:
            query = query.filter(db.or_(
                Usuarios.name.like(f'%{search}%'),
                Usuarios.email.like(f'%{search}%')
            ))
        total_filtered = query.count()

        # sorting
        order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = request.args.get(f'columns[{col_index}][data]')
            if col_name not in ['name', 'age', 'email']:
                col_name = 'name'
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(Usuarios, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1
        if order:
            query = query.order_by(*order)

        # pagination
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        query = query.offset(start).limit(length)

        # response
        # return {
        #     'data': [user.to_dict() for user in query],
        #     'recordsFiltered': total_filtered,
        #     'recordsTotal': Usuarios.query.count(),
        #     'draw': request.args.get('draw', type=int),
        # }

        jsonFinal = {
            "data": [user.to_dict() for user in query],
            "recordsFiltered": total_filtered,
            "recordsTotal": Usuarios.query.count(),
            "draw": request.args.get("draw", type=int),
        }

        # get string with all double quotes
        json_string = json.dumps(jsonFinal)

        # Forma 1 de devolver la data
        return json_string

        # Forma 2 de devolver la data
            # return Response(json_string, mimetype='application/json')

        # Forma 3 de devolver la data
            # respuesta = Response(response=json_string, status=200, mimetype="application/json")
            # respuesta.headers["Content-Type"] = "application/json; charset=utf-8"

