# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este modelo
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   app                 Es el aplicativo (app.py)
#   config              Mi archivo que guarda las configuraciones generales del aplicativo
#   datetime            Para manejar fechas y horas
#   sqlalchemy          ORM para SQL



from app import app  # El 1er app es el nombre del archivo app.py. El 2do "app" es la instancia de Flask() declarada en app.py
from config import *
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones. A través de esta sesión se va a gestionar las BD
Session = sessionmaker(engine)
sessionDB = Session()



class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())

    def getById(id):
        return sessionDB.query(Contacto).filter(
            Contacto.id == id
        ).first()

    def getByEmail(email):
        return sessionDB.query(Contacto).filter(
            Contacto.email == email
        ).first()

    def post(self):
        if not self.id:
            sessionDB.add(self)
        sessionDB.commit()

    def put(id, datos):
        sessionDB.query(Contacto).filter(Contacto.id == id).update({
            Contacto.nombre: datos['nombre'],
            Contacto.email: datos['email'],
            Contacto.telefono: datos['telefono']
        })
        sessionDB.commit()

    def delete(id):
        sessionDB.query(Contacto).filter(Contacto.id == id).delete()
        sessionDB.commit()

    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el email (no es que sólo contenga ese dato)
    def __str__(self):
        return self.email
