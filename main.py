from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.tasks import *
from forms.register import RegisterForm
from forms.login import LoginForm
import os
import random

CLASS_DICT = {9: Task9, 12: Task12, 10: Task10, 13: Task13, 15: Task15, 16: Task16}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
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
    return render_template("profile.html", title=f'Профиль {current_user.nickname}')


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
        f = form.picture.data
        f.save(os.path.join(os.getcwd(), f"static/img/avatars/{len(sess.query(User).all()) + 1}.jpg"))
        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            picture=f"{len(SESS.query(User).all()) + 1}.jpg"
        )
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
    random_tasks = SESS.query(CLASS_DICT[category]).filter(
        CLASS_DICT[category].done_by.notlike(f'%{current_user.id}%')).all()
    # print(len(random_tasks))
    if not random_tasks:
        return redirect(f"/congratulations/{category}")
    random_task = random.choice(random_tasks)
    return redirect(f"/category_task/{category}/task/{random_task.id}")


def main():
    app.run()


if __name__ == '__main__':
    main()
