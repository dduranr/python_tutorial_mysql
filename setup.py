# HACER QUE EL PROYECTO SEA INSTALABLE
# -----------------------------------------------------

# Nota
# En el tutorial esto se hace al final, pero en sus proyectos futuros siempre debe comenzar con esto.

# Hacer que su proyecto sea instalable significa que puede crear un archivo de distribución e instalarlo en otro entorno, tal como instaló Flask en el entorno de su proyecto. Esto hace que implementar su proyecto sea lo mismo que instalar cualquier otra biblioteca, por lo que está utilizando todas las herramientas estándar de Python para administrar todo.

# La instalación también viene con otros beneficios que pueden no ser obvios en el tutorial o como nuevo usuario de Python, que incluyen:

#   1. Actualmente, Python y Flask entienden cómo usar el paquete flaskr sólo porque está ejecutando desde el directorio de su proyecto. La instalación significa que puede importarlo sin importar desde dónde se ejecute.
#   2. Puede administrar las dependencias de su proyecto como lo hacen otros paquetes, así que instálelos con: pip install yourproject.whl
#   3. Las herramientas de prueba pueden aislar su entorno de prueba de su entorno de desarrollo.

# Este archivo (setup.py) describe su proyecto y los archivos que le pertenecen.

# packages le dice a Python qué directorios de paquetes incluir (y los archivos de Python que contienen). find_packages() encuentra estos directorios automáticamente para que no tenga que escribirlos. Para incluir otros archivos, como los directorios static y templates, se usa include_package_datase. Python necesita otro archivo con nombre MANIFEST.in para decir cuáles son estos otros datos.

# Lo que está en el MANIFEST.in le dice a Python que copie los directorios static y templates, y el archivo schema.sql, pero que excluya todos los archivos de código de bytes.



# INSTALAR EL PROYECTO
# -----------------------------------------------------
# Usar pip para instalar su proyecto en el entorno virtual.
#   pip install -e .
# Esto le dice a pip que busque setup.py en el directorio actual y lo instale en modo editable o de desarrollo. El modo editable significa que a medida que realiza cambios en su código local, sólo tendrá que volver a instalar si cambia los metadatos sobre el proyecto, como sus dependencias.

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)