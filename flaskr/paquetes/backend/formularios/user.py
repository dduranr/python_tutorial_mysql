from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserFormCreate(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	contrasena = StringField("Contrasena", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Crear")

class UserFormUpdate(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	# TODO Armar validador custom: contraseña no obligatoria pero si existe entonces que tenga al menos 8 caracteres, etc
	# contrasena = StringField("Contrasena", validators=[])
	submit = SubmitField("Actualizar")
