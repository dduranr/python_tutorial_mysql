from functools import wraps
from flask import abort, render_template
from flask_login import current_user


# cud_privileges_required = Privilegios de Create, Update and Delete obligatorios.
# Este decorador se encarga de permitir el acceso a la ruta indicada (a la que se decore), sólo a roles que tengan los privilegios de CUD. ¿Dónde se define qué roles tienen estos privilegios? Aquí en el decorador. Si el proyecto fuera más exigente y específico, podría crearse un decorador exclusivo para cada privilegio por separado.
# Parámetros:
#   elementoAcrear     String. Hace referencia al tipo de elemento a crear: blog, user, etc
def cud_privileges_required(elementoAcrear):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kws):
            # La variable 'rol' guarda el valor del atributo rol del usuario actual. Si por alguna razón current_user no tiene el atributo rol, se asigna el rol VIEWER como valor default
            rol = getattr(current_user, 'rol', 'viewer')
            error = 'Acceso denegado. No tienes el privilegio para acceder a esta sección'

            # Solamente los superadmin, admin y autor tienen privilegio de crear elementos
            if rol!='superadmin' and rol!='admin' and rol!='autor':
                return render_template('backend/errores/error.html', error=error)

            # Los autores sí tienen privilegio de ver el formulario de contacto, pero sólo del blog
            elif rol=='autor' and elementoAcrear!='blog':
                return render_template('backend/errores/error.html', error=error)

            return f(*args, **kws)
        return wrapper
    return decorate
