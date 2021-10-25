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


from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, or_
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import Column, Integer, String, DateTime
from flaskr.paquetes.backend.modelos.user import *
from sqlalchemy.dialects import postgresql
import os


SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones (sesión de BD, no sesión general del aplicativo que permite usar variables de sesión). A través de esta sesión se va a gestionar la BD.
Session = sessionmaker(engine)
sessionDB = Session()



class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer(), primary_key=True)
    author_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    contenido = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())




    # Este método se encarga de recuperar todos los posts de la tabla 'blog'. Recupera también los datos del user que creó cada post. Los parámetros son opcionales: si se ponen, devuelve los registros paginados; si no se ponen, devuelve todos los registros.
    # Esta es la query que ejecuta:
    #   SELECT * FROM blog b JOIN user u
    #   ON b.author_id = u.id
    #   LIMIT ? OFFSET ?
    # El método devuelve objetos, por lo que los datos se recuperan:
    #   {% for post in blogposts %}
    #       {{ post.blog.title }}
    #       {{ post.user.email }}
    #   {% endfor %}
    def getAll(row=0, rowperpage=0):
        t1 = aliased(Blog, name='blog')
        t2 = aliased(User, name='user')
        resultado = sessionDB.query(t1, t2).\
            slice(row, rowperpage).\
            all()

        # cadena1 = str(resultado.statement.compile(dialect=mysql.dialect()))
        cadena2 = str(resultado)
        # print('KKKKKKKKKKKKKKKKKKKK 1: ', cadena1)
        print('KKKKKKKKKKKKKKKKKKKK 2: ', cadena2)

        return resultado

    def getAll2(row=0, rowperpage=0, likeString=''):
        t1 = aliased(Blog, name='blog')
        t2 = aliased(User, name='user')
        return sessionDB.query(t1, t2).\
            filter(or_(
                Blog.title.like(likeString),
                Blog.contenido.like(likeString)
            )).\
            slice(row, rowperpage)

    # Este método recupera el número total de registros de la tabla blog
    def getCountWithoutFiltering():
        return sessionDB.query(Blog).count()

    # Este método recupera el número total de registros de la tabla blog, de acuerdo al filtro seleccionado
    def getCountWithFiltering(likeString):
        return sessionDB.query(Blog).filter(or_(
                Blog.title.like(likeString),
                Blog.contenido.like(likeString)
            )).\
            count()

    def getById(id):
        return sessionDB.query(Blog).filter(
            Blog.id == id
        ).first()

    def getByAuthorId(author_id):
        return sessionDB.query(Blog).filter(
            Blog.author_id == author_id
        ).first()

    def post(self):
        if not self.id:
            sessionDB.add(self)
        sessionDB.commit()

    def put(id, datos):
        sessionDB.query(Blog).filter(Blog.id == id).update({
            Blog.author_id: datos['author_id'],
            Blog.title: datos['title'],
            Blog.contenido: datos['contenido'],
        })
        sessionDB.commit()

    def delete(id):
        sessionDB.query(Blog).filter(Blog.id == id).delete()
        sessionDB.commit()

    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el title (no es que sólo contenga ese dato)
    def __str__(self):
        return self.title
