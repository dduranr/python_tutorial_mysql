from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class BlogFormCreate(FlaskForm):
	# Cada variable representa un campo de formulario
	title = StringField("Título", validators=[
		DataRequired(),
		Length(min=3)
	])
	img = FileField('Imagen', validators=[
		FileRequired(),
		FileAllowed(['jpg', 'png'], '¡Sólo se aceptan imágenes!')
	])
	contenido = TextAreaField("Contenido", default="Lorem ipsum dolor sit amet.", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Crear")

class BlogFormEdit(FlaskForm):
	author_id = IntegerField("Autor", validators=[
		DataRequired()
	])
	img = FileField("Imagen", validators=[
		FileRequired()
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
