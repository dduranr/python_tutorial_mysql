# data_name:    Nombre del campo en la fuente de datos
# column_name:  Name of the column in the table.
# default:      Value that will be displayed in case there's no data for the previous data_name.
# order:        Order of the column in the table.
# searchable:   Whether the column will be taken into account while searching a value.

# El key data_name puede tener como valor lo que sea, pero para tener un orden, lo mejor será numerarlos con letras de la A a la Z en mayúscula (que es como venía originalmente).
# En la línea 72 aprox del serverside_table.py se hace referencia al data_name que aquí contiene el ID de los registros. En ese archivo se asume que el ID siempre aparecerá, y que lo hará en la columna A.

USERS = [
    {
        "data_name": "A",
        "column_name": "ID",
        "default": "",
        "order": 1,
        "searchable": True
    },
    {
        "data_name": "B",
        "column_name": "NOMBRE",
        "default": "",
        "order": 2,
        "searchable": True
    },
    {
        "data_name": "C",
        "column_name": "EMAIL",
        "default": 0,
        "order": 3,
        "searchable": False
    }
]

BLOG = [
    {
        "data_name": "A",
        "column_name": "ID",
        "default": "",
        "order": 1,
        "searchable": True
    },
    {
        "data_name": "B",
        "column_name": "AUTOR",
        "default": "",
        "order": 2,
        "searchable": True
    },
    {
        "data_name": "C",
        "column_name": "TÍTULO",
        "default": "",
        "order": 3,
        "searchable": True
    },
    {
        "data_name": "D",
        "column_name": "CREADO",
        "default": 0,
        "order": 5,
        "searchable": False
    }
]

CONTACTO = [
    {
        "data_name": "A",
        "column_name": "ID",
        "default": "",
        "order": 1,
        "searchable": True
    },
    {
        "data_name": "B",
        "column_name": "NOMBRE",
        "default": "",
        "order": 2,
        "searchable": True
    },
    {
        "data_name": "C",
        "column_name": "EMAIL",
        "default": "",
        "order": 3,
        "searchable": True
    },
    {
        "data_name": "D",
        "column_name": "CREADO",
        "default": 0,
        "order": 5,
        "searchable": False
    }
]
