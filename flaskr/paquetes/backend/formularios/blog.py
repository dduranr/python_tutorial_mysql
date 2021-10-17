from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BlogFormCreate(FlaskForm):
	# Cada variable representa un campo de formulario
	title = StringField("Título", validators=[
		DataRequired(),
		Length(min=3)
	])
	contenido = StringField("Contenido", validators=[
		DataRequired(),
		Length(min=3)
	])
	submit = SubmitField("Crear")
