from flaskr.paquetes.backend.serverside.serverside_table import ServerSideTable
from flaskr.paquetes.backend.serverside import table_schemas
from sqlalchemy.sql import func
from sqlalchemy import create_engine, exc, Column, Integer, String, DateTime, asc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os



# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones (sesión de BD, no sesión general del aplicativo que permite usar variables de sesión). IMPORTANTE: Esto se hace una sola vez en todo el aplicativo (la variable sessionDB estará disponible automáticamente en el resto de modelos)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
session_factory = sessionmaker(bind=engine)
sessionDB = scoped_session(session_factory)



class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=func.now())
    updated_at = Column(DateTime(255), default=func.now(), onupdate=func.now())



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
        engine.dispose()
        sessionDB.query(User).filter(User.id == id).update({
            User.nombre: datos['nombre'],
            User.email: datos['email'],
            User.contrasena: datos['contrasena'],
            User.rol: datos['rol']
        })
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()



    # Este método elimina un registro
    # Params:
    #   id     Int. Identificador del registro
    def delete(id):
        sessionDB.query(User).filter(User.id == id).delete()
        sessionDB.commit()



    # Este método establece la contraseña
    # Params:
    #   self        Obj. El objeto usuario al que se le establecerá la contraseña
    #   password    Str. La contraseña
    def set_password(self, password):
        """Create hashed password."""
        self.contrasena = generate_password_hash(
            password,
            method='sha256'
        )



    # Este método checa si la contraseña introducida coincide con a de la BD
    # Params:
    #   self        Obj. El objeto usuario al que se le establecerá la contraseña
    #   password    Str. La contraseña
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.contrasena, password)



    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
