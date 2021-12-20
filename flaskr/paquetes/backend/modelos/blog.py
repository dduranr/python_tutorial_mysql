from flaskr.paquetes.backend.serverside.serverside_table import ServerSideTable
from flaskr.paquetes.backend.serverside import table_schemas
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc, or_, Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from flaskr.paquetes.backend.modelos.user import *
from sqlalchemy.dialects import postgresql
import os


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer(), primary_key=True)
    author_id = Column(Integer(), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    contenido = Column(String(255), nullable=False)
    img = Column(String(10), nullable=True)
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


    # Este método recupera todos los registros
    # Params:
    #   orderby     String. Opcional. Ordena los resultados por el nombre de la columna pasada aquí. Si no se proporciona, se ordena por ID.
    def getAll(orderby="id"):
        engine.dispose()
        res = sessionDB.query(Blog).order_by(asc(orderby)).all()
        sessionDB.close()
        sessionDB.remove()
        return res


    # Este método recupera un registro según su ID
    # Params:
    #   id     Int. Identificador del registro
    def getById(id):
        engine.dispose()
        blog = aliased(Blog)
        user = aliased(User)
        query = (
            sessionDB.query(user, blog)
            .select_from(blog)
            .join(user, user.id == blog.author_id)
            .filter(blog.id == id)
        )
        res = query.one_or_none()

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
        sessionDB.query(Blog).filter(Blog.id == id).update({
            Blog.author_id: datos['author_id'],
            Blog.title: datos['title'],
            Blog.contenido: datos['contenido'],
            Blog.img: datos['img'],
        })
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()


    # Este método elimina un registro
    # Params:
    #   id     Int. Identificador del registro
    def delete(id):
        engine.dispose()
        sessionDB.query(Blog).filter(Blog.id == id).delete()
        sessionDB.commit()
        sessionDB.close()
        sessionDB.remove()


    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el title (no es que sólo contenga ese dato)
    def __str__(self):
        return self.title
