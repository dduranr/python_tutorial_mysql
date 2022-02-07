from flaskr.paquetes.backend.serverside import table_schemas
from flaskr.paquetes.backend.serverside.serverside_table import ServerSideTable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc, or_, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from flaskr.paquetes.backend.modelos.user import *
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
import os


class Contacto(Base):
    __tablename__ = 'submissions'

    id = Column(Integer(), primary_key=True)
    forma = Column(String(255), nullable=False)
    datos = Column(String(), nullable=False)
    created_at = Column(DateTime(255), default=func.now())


    # Este método se encarga de recuperar los datos que van a parar al datatables
    def collect_data_serverside(self, request):
        engine.dispose()
        DATA = []
        query = sessionDB.query(Contacto)
        for c in query.all():
            DATA.append({'A': c.id, 'B': c.datos, 'C': c.created_at})
        columns = table_schemas.CONTACTO
        sessionDB.close()
        sessionDB.remove()
        return ServerSideTable(request, DATA, columns, False, False, '', 'A', 'table_contacto').output_result()



    # Este método recupera todos los registros
    # Params:
    #   orderby     String. Opcional. Ordena los resultados por el nombre de la columna pasada aquí
    #   ascendente  Bool. Opcional. Ordena los resultados por ASC si es True, por DESC si es False
    def getAll(orderby="id", ascendente=True):
        engine.dispose()

        query = sessionDB.query(Contacto)

        ordenamiento = None
        if orderby == 'id':
            if ascendente:
                ordenamiento = contacto.id.asc()
            else:
                ordenamiento = contacto.id.desc()
        elif orderby == 'created_at':
            if ascendente:
                ordenamiento = contacto.created_at.asc()
            else:
                ordenamiento = contacto.created_at.desc()

        res = query.order_by(ordenamiento).all()

        sessionDB.close()
        sessionDB.remove()
        return res



    # Este método crea nuevo registro
    # Params:
    #   self     Obj. Es el propio registro, y ya debe traer los datos a guardar
    def post(self):
        engine.dispose()
        if not self.id:
            sessionDB.add(self)
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()



    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
