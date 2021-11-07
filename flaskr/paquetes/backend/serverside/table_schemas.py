# data_name:    Nombre del campo en la fuente de datos
# column_name:  Name of the column in the table.
# default:      Value that will be displayed in case there's no data for the previous data_name.
# order:        Order of the column in the table.
# searchable:   Whether the column will be taken into account while searching a value.

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
    },
    {
        "data_name": "D",
        "column_name": "CREADO",
        "default": 0,
        "order": 4,
        "searchable": False
    }
]
