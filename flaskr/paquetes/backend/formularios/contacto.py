from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ContactoForm(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=3)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	mensaje = TextAreaField("Mensaje", default="", validators=[
		DataRequired(),
		Length(min=3)
	])
	documento = FileField('Documento', validators=[
		FileAllowed(['jpg', 'jpeg', 'png'], 'El archivo a subir no corresponde con un tipo permitido de imagen (sólo se permiten JPG y PNG).')
	])
	forma = HiddenField("forma", default="contacto", validators=[
		DataRequired()
	])
