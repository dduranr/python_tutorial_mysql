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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc, or_, Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flaskr.paquetes.backend.modelos.user import *
from sqlalchemy.dialects import postgresql
import os


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer(), primary_key=True)
    author_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    contenido = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())


    # Este método se encarga de recuperar los datos que van a parar al datatables
    def collect_data_serverside(self, request):
        engine.dispose()
        DATA = []
        query = sessionDB.query(User, Blog).filter(User.id==Blog.author_id)
        for u, b in query.all():
            DATA.append({'A': b.id, 'B': u.nombre, 'C': b.title, 'D': b.created_at})
        columns = table_schemas.BLOG
        sessionDB.close()
        sessionDB.remove()
        return ServerSideTable(request, DATA, columns, True, True, 'backend.blog', 'C', 'table_blogposts').output_result()

    def getAll():
        engine.dispose()
        res = sessionDB.query(Blog).all()
        sessionDB.close()
        sessionDB.remove()
        return res

    # Este método recupera el número total de registros de la tabla blog
    def getCountWithoutFiltering():
        engine.dispose()
        res = sessionDB.query(Blog).count()
        sessionDB.close()
        sessionDB.remove()
        return res

    # Este método recupera el número total de registros de la tabla blog, de acuerdo al filtro seleccionado
    def getCountWithFiltering(likeString):
        engine.dispose()
        res = sessionDB.query(Blog).filter(or_(
                Blog.title.like(likeString),
                Blog.contenido.like(likeString)
            )).\
            count()
        sessionDB.close()
        sessionDB.remove()
        return res

    def getById(id):
        engine.dispose()
        res = sessionDB.query(Blog).filter(Blog.id == id).first()
        sessionDB.close()
        sessionDB.remove()
        return res

    def getByAuthorId(author_id):
        engine.dispose()
        res = sessionDB.query(Blog).filter(Blog.author_id == author_id).first()
        sessionDB.close()
        sessionDB.remove()
        return res

    def post(self):
        engine.dispose()
        if not self.id:
            sessionDB.add(self)
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()

    def put(id, datos):
        engine.dispose()
        sessionDB.query(Blog).filter(Blog.id == id).update({
            Blog.author_id: datos['author_id'],
            Blog.title: datos['title'],
            Blog.contenido: datos['contenido'],
        })
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()

    def delete(id):
        engine.dispose()
        sessionDB.query(Blog).filter(Blog.id == id).delete()
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()


    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el title (no es que sólo contenga ese dato)
    def __str__(self):
        return self.title
