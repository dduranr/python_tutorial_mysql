from flask_wtf import FlaskForm
from flaskr.paquetes.general.constantes import Constantes
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError
import re

passPatron = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,100}$'
passErrorMsg = 'La contraseña no es lo suficientemente fuerte. '+Constantes.REQUISITOS_CONTRASENA

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
	# Para la contraseña armamos un validador custom basado en una expresión regular (la contraseña es obligatoria)
	contrasena = StringField("Contraseña", validators=[])
	def validate_contrasena(form, field):
		if len(field.data) > 0:
			if re.fullmatch(r''+passPatron, field.data):
				return True
			else:
				raise ValidationError(passErrorMsg)
		else:
			raise ValidationError('La contraseña es obligatoria.')
	rol = SelectField(
		u'Rol',
		validators=[DataRequired()],
		choices=[
			('', ':: Elige ::'),
			('admin', 'Administrador'),
			('editor', 'Editor')
		]
	)
	submit = SubmitField("Crear")


	# No sé por qué puse este método aquí. No se usa en ningún lado
	# def edit_user(request, id):
	# 	user = User.query.get(id)
	# 	form = UserDetails(request.POST, obj=user)
	# 	form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]


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
	# Para la contraseña armamos un validador custom basado en una expresión regular (la contraseña es opcional)
	contrasena = StringField("Contraseña", validators=[])
	def validate_contrasena(form, field):
		if len(field.data) > 0:
			if re.fullmatch(r''+passPatron, field.data):
				return True
			else:
				raise ValidationError(passErrorMsg)
	rol = SelectField(
		u'Rol',
		validators=[DataRequired()],
		choices=[
			('', ':: Elige ::'),
			('admin', 'Administrador'),
			('editor', 'Editor')
		]
	)
	submit = SubmitField("Actualizar")
