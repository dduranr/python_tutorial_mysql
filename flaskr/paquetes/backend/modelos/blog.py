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
from sqlalchemy import create_engine, exc, or_
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import Column, Integer, String, DateTime
from flaskr.paquetes.backend.modelos.user import *
from sqlalchemy.dialects import postgresql
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

        # FORMA 1
        # t1 = aliased(Blog, name='blog')
        # t2 = aliased(User, name='user')
        # resultado = sessionDB.query(t1, t2).filter(t1.author_id == User.id).all()

        # FORMA 2
        # resultado = (sessionDB.query(User,Blog)
        #     .filter(Blog.author_id == User.id)
        #     .all())

        # FORMA 3
        # resultado = sessionDB.query(Blog).join(User).filter(Blog.author_id == User.id)
        # resultado = sessionDB.query(Blog).join(User, Blog.author_id == User.id)

        # FORMA 4
        DATA = []
        query = sessionDB.query(User, Blog).filter(User.id==Blog.author_id)
        # print('------------------------------')
        # print("SQL: {0}".format(query))
        # print('REGISTROS TOTALES: ', len(query.all()))
        # print('------------------------------')
        for u, b in query.all():
            DATA.append({'A': b.id, 'B': u.nombre, 'C': b.title, 'D': b.created_at})
        columns = table_schemas.BLOG
        return ServerSideTable(request, DATA, columns, True, True, 'backend.blog', 'C', 'table_blogposts').output_result()


    def getAll():
        return sessionDB.query(Blog).all()

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
    # def getAll(row=0, rowperpage=0):
    #     t1 = aliased(Blog, name='blog')
    #     t2 = aliased(User, name='user')
    #     resultado = sessionDB.query(t1, t2).\
    #         slice(row, rowperpage).\
    #         all()

    #     cadena2 = str(resultado)
    #     return resultado

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
        sessionDB.remove()


    # Cuando se hace print() al objeto devuelto por esta clase, por defecto devolverá el title (no es que sólo contenga ese dato)
    def __str__(self):
        return self.title
