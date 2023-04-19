from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class RedactForm(FlaskForm):
    nickname = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    picture = FileField('Выбрать аватар')
    submit = SubmitField("Редактировать")
