from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
