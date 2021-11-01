# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este modelo
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   app                 Es el aplicativo (app.py)
#   config              Mi archivo que guarda las configuraciones generales del aplicativo
#   datetime            Para manejar fechas y horas
#   sqlalchemy          ORM para SQL

from flaskr.paquetes.backend.serverside.serverside_table import ServerSideTable
from flaskr.paquetes.backend.serverside import table_schemas

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import os


SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones (sesión de BD, no sesión general del aplicativo que permite usar variables de sesión). A través de esta sesión se va a gestionar la BD.
Session = sessionmaker(engine)
sessionDB = Session()

# DATA_SAMPLE = [
#     {'A': 'Hello!', 'B': 'How is it going?', 'C': 3, 'D': 4},
#     {'A': 'These are sample texts', 'B': 0, 'C': 5, 'D': 6},
#     {'A': 'Mmmm', 'B': 'I do not know what to say', 'C': 7, 'D': 16},
#     {'A': 'Is it enough?', 'B': 'Okay', 'C': 8, 'D': 9},
#     {'A': 'Just one more', 'B': '...', 'C': 10, 'D': 11},
#     {'A': 'Thanks!', 'B': 'Goodbye.', 'C': 12, 'D': 13}
# ]


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())


    def collect_data_serverside(self, request):

        usersDB = User.getAll()
        DATA_SAMPLE = []

        for usuario in usersDB:
            DATA_SAMPLE.append({'A': usuario.id, 'B': usuario.nombre, 'C': usuario.email, 'D': usuario.created_at})


        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, DATA_SAMPLE, columns).output_result()

    def get20():
        return sessionDB.query(User).limit(20).all()

    def getAll():
        return sessionDB.query(User).all()

    def queryCount():
        return sessionDB.query(User).count()

    def queryOrderBy(order):
        return sessionDB.query(User).order_by(*order)

    def getById(id):
        return sessionDB.query(User).filter(
            User.id == id
        ).first()

    def getByEmail(email):
        return sessionDB.query(User).filter(
            User.email == email
        ).first()

    def post(self):
        if not self.id:
            sessionDB.add(self)
        sessionDB.commit()

    def put(id, datos):
        sessionDB.query(User).filter(User.id == id).update({
            User.nombre: datos['nombre'],
            User.email: datos['email'],
            User.contrasena: datos['contrasena']
        })
        sessionDB.commit()

    def delete(id):
        sessionDB.query(User).filter(User.id == id).delete()
        sessionDB.commit()

    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
