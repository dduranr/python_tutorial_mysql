# Este controlador se encarga de gestionar el contenido que va a parar a los datatables

from flask import Blueprint, request, jsonify
from flaskr.paquetes.backend.modelos.user import User


modeloUser = User()


bp = Blueprint('datatables', __name__, url_prefix='/datatables')

@bp.route("/serverside_table/<tabla>", methods=['GET'])
def serverside_table_content(tabla):
    data = None
    if tabla=='users':
        data = modeloUser.collect_data_serverside(request)

    return jsonify(data)
