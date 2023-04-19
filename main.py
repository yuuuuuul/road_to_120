from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session, tasks_resource, users_resource
from data.users import User
from data.tasks import *
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.redact import RedactForm
from forms.change_password import ChangePasswordForm
from forms.add_tasks import AddTaskForm
import os
import random

CLASS_DICT = {4: Task4, 5: Task5, 6: Task6, 7: Task7, 9: Task9, 10: Task10, 11: Task11, 12: Task12, 13: Task13,
              14: Task14, 15: Task15, 16: Task16, 17: Task17, 18: Task18, 21: Task21}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

api.add_resource(tasks_resource.TasksResource, "/api/tasks/<int:category_id>/<int:task_id>")
api.add_resource(tasks_resource.TasksListResource, "/api/tasks/<int:category_id>")
api.add_resource(users_resource.UsersResource, "/api/users/<int:user_id>")
api.add_resource(users_resource.UsersListResource, "/api/users")

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/ege_russian_project.db")
SESS = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    return SESS.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    find_picture = False
    if current_user.picture:
        find_picture = True
    return render_template("profile.html", title=f'Профиль {current_user.nickname}', find_picture=find_picture)


@app.route("/password_change", methods=["GET", "POST"])
@login_required
def password_change():
    form = ChangePasswordForm()
    user = SESS.query(User).filter(User.id == current_user.id).first()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("change_password.html", title="Смена пароля", form=form,
                                   message="Пароли не совпадают")
        user.set_password(form.password.data)
        SESS.commit()
        return redirect("/profile")
    return render_template("change_password.html", title="Смена пароля", form=form)


@app.route("/profile_redact", methods=['GET', 'POST'])
@login_required
def profile_redact():
    form = RedactForm()
    user = SESS.query(User).filter(User.id == current_user.id).first()
    if request.method == 'GET':
        form.nickname.data = user.nickname
        form.email.data = user.email
        form.picture.data = user.picture
    if form.validate_on_submit():
        if SESS.query(User).filter((User.email == form.email.data) & (User.id != user.id)).first():
            return render_template("redact.html", title="Редактирование информации",
                                   form=form, message="Пользователь с данной почтой уже существует")
        if SESS.query(User).filter((User.nickname == form.nickname.data) & (User.id != user.id)).first():
            return render_template("redact.html", title="Редактирование информации",
                                   form=form, message="Пользователь с данным именем уже существует")
        user.nickname = form.nickname.data
        user.email = form.email.data
        f = form.picture.data
        if f.filename:
            f.save(os.path.join(os.getcwd(), f"static/img/avatars/{user.id}.jpg"))
        SESS.commit()
        return redirect("/profile")
    return render_template("redact.html", title="Редактирование информации",
                           form=form)


@app.route("/add_task", methods=['GET', "POST"])
@login_required
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        if not form.category.data in CLASS_DICT.keys():
            return render_template("add_tasks.html", title="Добавление задания", form=form,
                                   message="Категория не найдена")
        new_task = CLASS_DICT[form.category.data](
            text_of_the_task=form.text_of_the_task.data,
            answers=form.answers.data,
            adding=form.adding.data
        )
        SESS.add(new_task)
        SESS.commit()
        return redirect("/")
    return render_template("add_tasks.html", title="Добавление задания", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = SESS.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template("login.html", title='Авторизация', form=form,
                               message="Неверный логин или пароль")
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пароли не совпадают')
        if SESS.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пользователь с данной почтой уже есть')
        user = User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        f = form.picture.data
        if f.filename:
            f.save(os.path.join(os.getcwd(), f"static/img/avatars/{len(SESS.query(User).all()) + 1}.jpg"))
            user.picture = f"{len(SESS.query(User).all()) + 1}.jpg"
        user.set_password(form.password.data)
        SESS.add(user)
        SESS.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=["GET", "POST"])
def main_screen():
    if request.method == "GET":
        return render_template("main.html", title="Главный экран")
    elif request.method == "POST":
        category_of_task = int(request.form["task"])
        if not category_of_task:
            return render_template("main.html", title="Главный экран", message="Выберите категорию задания")
        # print(category_of_task)
        return get_task(category_of_task)


@app.route("/congratulations/<int:category>", methods=["GET"])
@login_required
def congratulations(category):
    return render_template("congratulations.html", title="Поздравляем!", category=category)


@app.route("/example_task", methods=["GET"])
def example_task():
    category = 12
    task = SESS.query(CLASS_DICT[category]).get(1)
    return render_template('example_task.html', title="Пример задания", category=category, task=task,
                           message="Пример задания! Для проверки ответов зарегистрируйтесь/авторизуйтесь на сайте :)")


@app.route("/category_task/<int:category>/task/<int:id_task>", methods=["GET", "POST"])
@login_required
def show_task(category, id_task):
    task = SESS.query(CLASS_DICT[category]).get(id_task)
    # print(task.text_of_the_task)
    if request.method == "GET":
        return render_template("task.html", title=f"Задание {category}.{id_task}", task=task, category=category)
    elif request.method == "POST":
        # print(request.form)
        if "answer" in request.form:
            ans = set(request.form["answer"].replace(" ", ""))
            if not (ans == set(task.answers)):
                return render_template("task.html", title=f"Задание {category}.{id_task}",
                                       task=task, category=category, message="Вы ошиблись :(", is_right=-1)
            task.done_by = f"{task.done_by}, {current_user.id}" if task.done_by else current_user.id
            SESS.query(User).get(current_user.id).task_completed += 1
            SESS.commit()
            return render_template("task.html", title=f"Задание {category}.{id_task}",
                                   task=task, category=category, message="Вы ответили верно!", is_right=1)
        elif "hint" in request.form:
            return render_template("task.html", title=f"Задание {category}.{id_task}",
                                   task=task, category=category, message="Вы ошиблись :(", is_right=-1, is_hint=True)
        elif "new_task" in request.form:
            return get_task(category)


def get_task(category):
    random_tasks = SESS.query(CLASS_DICT[category]).all()
    # print(len(random_tasks))
    random.shuffle(random_tasks)
    for task in random_tasks:
        if not task.done_by or not (str(current_user.id) in task.done_by):
            return redirect(f"/category_task/{category}/task/{task.id}")
    return redirect(f"/congratulations/{category}")


def main():
    app.run()


if __name__ == '__main__':
    main()
