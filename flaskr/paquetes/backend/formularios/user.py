from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError
import re

passPatron = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,100}$'
passErrorMsg = 'La contraseña no es lo suficientemente fuerte. Debe contener una letra mayúscula, una minúscula, un número, un caracter especial y al menos 8 dígitos (máximo 100).'

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
	# Para la contraseña armamos un validador custom basado en una expresión regular
	contrasena = StringField("Contraseña", validators=[])
	def validate_contrasena(form, field):
		# La contraseña es opcional, pero si el usuario la pone entonces debe cumplir con requisitos
		if len(field.data) > 0:
			if re.fullmatch(r''+passPatron, field.data):
				return True
			else:
				raise ValidationError(passErrorMsg)
		else:
			raise ValidationError('La contraseña es obligatoria.')
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

	# Para la contraseña armamos un validador custom basado en una expresión regular
	contrasena = StringField("Contraseña", validators=[])
	def validate_contrasena(form, field):
		# La contraseña es opcional, pero si el usuario la pone entonces debe cumplir con requisitos
		if len(field.data) > 0:
			if re.fullmatch(r''+passPatron, field.data):
				return True
			else:
				raise ValidationError(passErrorMsg)

	submit = SubmitField("Actualizar")
