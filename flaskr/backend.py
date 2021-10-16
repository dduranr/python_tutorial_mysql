# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Este blueprint sólo tiene como objetivo agregar a las rutas del backend el prefijo "backend".
# Es decir, se van a armar blueprints anidados, de tal modo que el blueprint padre será este de "backend".
# Por eso no tiene funciones ni nada.
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

from flask import Blueprint
bp = Blueprint('backend', __name__, url_prefix='/backend')
