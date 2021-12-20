from os import environ
from datetime import datetime
import logging, logging.config



# Esta función se encarga de armar una cadena HTML con los errores devueltos cuando no valida un formulario WTForms. Params:
#   errores. Diccionario. Corresponde con el diccionario devuelto por formularioWTForms.errors
def getErrorsFromWTF(errores):
    r = '<ul>'
    for err in errores:
        errValues = errores[err]
        r += '<li><small>'+err.capitalize()+': '
        for errValue in errValues:
            r += errValue+'</small></li>'
    r += '</ul>'
    return r



# Esta función se encarga de armar toda la configuración relacionada con guardar los logs en archivos de texto. Devuelve el logger, que es el que permite hacer los logs.
# Uso: simplemente se instancia logger = fileLogSystem() y se genera log: logger.exception(error)
def fileLogSystem():
    FOLDER_ROOT = environ.get('FOLDER_ROOT')
    FOLDER_LOGS = environ.get('FOLDER_LOGS')

    logging.config.fileConfig(FOLDER_ROOT+'\\log.ini')
    logger = logging.getLogger('MainLogger')

    fh = logging.FileHandler(FOLDER_LOGS+'\\{:%Y%m%d}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(filename)s (%(lineno)04d): %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

