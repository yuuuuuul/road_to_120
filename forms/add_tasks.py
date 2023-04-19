from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    category = IntegerField("Категория", validators=[DataRequired()])
    text_of_the_task = StringField("Задание", validators=[DataRequired()])
    answers = StringField("Ответ на задание", validators=[DataRequired()])
    adding = StringField("Подсказка", validators=[DataRequired()])
    submit = SubmitField("Добавить")
