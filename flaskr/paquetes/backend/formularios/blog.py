from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class BlogFormCreate(FlaskForm):
	# Cada variable representa un campo de formulario
	title = StringField("Título", validators=[
		DataRequired(),
		Length(min=3)
	])
	contenido = TextAreaField("Contenido", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Crear")

class BlogFormEdit(FlaskForm):
	author_id = IntegerField("Autor", validators=[
		DataRequired()
	])
	title = StringField("Título", validators=[
		DataRequired(),
		Length(min=3)
	])
	contenido = TextAreaField("Contenido", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Actualizar")
