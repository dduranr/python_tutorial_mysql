# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


from flask import Blueprint, request, jsonify
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from flaskr.paquetes.backend.modelos.user import User
from datetime import datetime
import functools
import json


modeloUser = User()


bp = Blueprint('userDatatables', __name__, url_prefix='/userDatatables')

@bp.route("/serverside_table", methods=['GET'])
def serverside_table_content():
    data = modeloUser.collect_data_serverside(request)
    return jsonify(data)
