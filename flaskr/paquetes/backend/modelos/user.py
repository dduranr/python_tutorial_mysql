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
from sqlalchemy import create_engine, exc, Column, Integer, String, DateTime, asc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os



# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones (sesión de BD, no sesión general del aplicativo que permite usar variables de sesión). IMPORTANTE: Esto se hace una sola vez en todo el aplicativo (la variable sessionDB estará disponible automáticamente en el resto de modelos)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
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


    # Este método recupera todos los usuarios
    # Params:
    #   orderby     String. Opcional. Ordena los resultados por el nombre de la columna pasada aquí. Si no se proporciona, se ordena por ID.
    def getAll(orderby="id"):
        engine.dispose()
        res = sessionDB.query(User).order_by(asc(orderby)).all()
        sessionDB.close()
        sessionDB.remove()
        return res


    # Este método recupera un registro según su ID
    # Params:
    #   id     Int. Identificador del registro
    def getById(id):
        engine.dispose()
        res = sessionDB.query(User).filter(User.id == id).one_or_none()
        sessionDB.close()
        sessionDB.remove()
        return res


    # Este método recupera un registro según su EMAIL
    # Params:
    #   email     String. Email del registro
    def getByEmail(email):
        engine.dispose()
        res = sessionDB.query(User).filter(User.email == email).one_or_none()
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


    # Este método actualiza registro
    # Params:
    #   id     Int. Identificador del registro
    #   datos  Obj. Datos a actualizar
    def put(id, datos):
        sessionDB.query(User).filter(User.id == id).update({
            User.nombre: datos['nombre'],
            User.email: datos['email'],
            User.contrasena: datos['contrasena']
        })
        sessionDB.commit()


    # Este método elimina un registro
    # Params:
    #   id     Int. Identificador del registro
    def delete(id):
        sessionDB.query(User).filter(User.id == id).delete()
        sessionDB.commit()


    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
