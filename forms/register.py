from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    picture = FileField('Выбрать аватар')
    submit = SubmitField("Зарегистрироваться")
