from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Email, Length


class AuthFormLogin(FlaskForm):
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	contrasena = StringField("Contrasena", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Entrar")
	recaptcha = RecaptchaField(validators=[
		Recaptcha(message="El captcha no fue contestado satisfactoriamente.")
	])
