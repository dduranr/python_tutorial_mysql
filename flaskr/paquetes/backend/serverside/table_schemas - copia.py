# data_name:    Nombre del campo en la fuente de datos
# column_name:  Name of the column in the table.
# default:      Value that will be displayed in case there's no data for the previous data_name.
# order:        Order of the column in the table.
# searchable:   Whether the column will be taken into account while searching a value.


SERVERSIDE_TABLE_COLUMNS = [
    {
        "data_name": "name",
        "column_name": "Name",
        "default": "",
        "order": 1,
        "searchable": False
    },
    {
        "data_name": "age",
        "column_name": "Age",
        "default": "",
        "order": 2,
        "searchable": True
    },
    {
        "data_name": "address",
        "column_name": "Address",
        "default": 0,
        "order": 3,
        "searchable": True
    },
    {
        "data_name": "phone",
        "column_name": "Phone",
        "default": 0,
        "order": 4,
        "searchable": True
    },
    {
        "data_name": "email",
        "column_name": "Email",
        "default": 0,
        "order": 5,
        "searchable": True
    }
]
