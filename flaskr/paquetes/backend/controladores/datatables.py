# Este controlador se encarga de gestionar el contenido que va a parar a los datatables

from flask import Blueprint, request, jsonify
from flaskr.paquetes.backend.modelos.user import User
from flaskr.paquetes.backend.modelos.blog import Blog
from flaskr.paquetes.backend.modelos.contacto import Contacto


modeloUser = User()
modeloBlog = Blog()
modeloContacto = Contacto()


bp = Blueprint('datatables', __name__, url_prefix='/datatables')

@bp.route("/serverside_table/<tabla>", methods=['GET'])
def serverside_table(tabla):
    data = None
    if tabla=='users':
        data = modeloUser.collect_data_serverside(request)
    elif tabla=='blog':
        data = modeloBlog.collect_data_serverside(request)
    elif tabla=='submissions':
        data = modeloContacto.collect_data_serverside(request)

    return jsonify(data)
