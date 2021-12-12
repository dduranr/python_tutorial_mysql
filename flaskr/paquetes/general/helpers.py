# import os
from os import environ
from datetime import datetime
import logging, logging.config

# Cuando un formulario WTForms no valida bien, a veces me veo en la necesidad de hacer un redirect (en lugar de hacer un render_template), con lo cual los errores WTF no se plasman debajo de cada campo del formulario, es decir, se pierden. En cualquier caso siempre devuelvo un flash(). La idea es que en este flash se muestren siempre los errores que devuelve WTF (si los hay). Esta función se encarga de recuperar esos errores y devolverlos en una cadena. Params:
#   errores. Diccionario. Corresponde con el diccionario formularioWTForms.errors
def getErrorsFromWTF(errores):
    r = '<ul>'
    for err in errores:
        errValues = errores[err]
        r += '<li><small>'+err.capitalize()+': '
        for errValue in errValues:
            r += errValue+'</small></li>'
    r += '</ul>'
    return r

def getSystemLog():
    FOLDER_ROOT = environ.get('FOLDER_ROOT')
    FOLDER_LOGS = environ.get('FOLDER_LOGS')

    logging.config.fileConfig(FOLDER_ROOT+'\\log.ini')
    logger = logging.getLogger('MainLogger')

    fh = logging.FileHandler(FOLDER_LOGS+'\\{:%Y%m%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(filename)s (%(lineno)04d): %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

