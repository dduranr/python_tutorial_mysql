# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este modelo
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   app                 Es el aplicativo (app.py)
#   config              Mi archivo que guarda las configuraciones generales del aplicativo
#   datetime            Para manejar fechas y horas
#   sqlalchemy          ORM para SQL
#       create_engine
#       exc             Para poder recuperar los errores devueltos
#       or_             Sirve para implementar el operador OR dentro del filter


from flaskr.paquetes.backend.serverside.serverside_table import ServerSideTable
from flaskr.paquetes.backend.serverside import table_schemas
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import os



# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones (sesión de BD, no sesión general del aplicativo que permite usar variables de sesión). A través de esta sesión se va a gestionar la BD. Al trabajar con AJAX para borrar registros, en su momento SQLAlchemy me devolvía alternativamente estos errores:
#   1. 2014, "Commands out of sync
#   2. This session is in 'prepared' state; no further SQL can be emitted within this transaction
#   3. Can't reconnect until invalid transaction is rolled back
# Esto estaba relacionado con 2 problemas distintos:
#   1. En el controlador estaba recuperando datos del registro a eliminar, pero algo pasaba con SQLAlchemy que decía que no recuperaba el registro cuando sí existía, por lo que parte de los problemas se arregló haciendo más puntual mis comprobaciones de existencia del registro:
#       userExistente = User.getById(id)
#       booleano = bool(userExistente)
#       userNombre = '?'
#       if booleano:
#           userNombre = userExistente.nombre
#   2. En el modelo (o sea aquí) no estaba usando sesiones contextuales:
#       Session = sessionmaker(engine)
#       sessionDB = Session()
#       La cosa se solucionó usando scoped_session(), ver: https://stackoverflow.com/questions/69979098/commands-out-of-sync-error-in-python-with-sqlalchemy?noredirect=1#comment123703037_69979098. Para ser más exactos, la cosa se solucionó al 99%, porque si ahora borro un registro tras otro, quizá pueda eliminar unos 10-15 registros sin problema, pero después de eso datatables se queda en "processing". Esto es otro error y no sé en dónde radique el problema, y de hecho si dejo de eliminar registros el datatables termina por reaccionar. De cualquier modo, este problema es menor.

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine)
sessionDB = scoped_session(session_factory)



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())


    # Este método se encarga de recuperar los datos que van a parar al datatables
    def collect_data_serverside(self, request):
        usersDB = User.getAll()
        DATA = []
        for usuario in usersDB:
            DATA.append({'A': usuario.id, 'B': usuario.nombre, 'C': usuario.email, 'D': usuario.created_at})

        columns = table_schemas.USERS
        return ServerSideTable(request, DATA, columns, True, True, 'backend.user', 'B', 'table_users').output_result()

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
        sessionDB.remove()

    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
