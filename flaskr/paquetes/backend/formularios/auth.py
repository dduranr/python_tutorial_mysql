from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AuthFormLogin(FlaskForm):
	# Cada variable representa un campo de formulario
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	contrasena = StringField("Contrasena", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Entrar")
