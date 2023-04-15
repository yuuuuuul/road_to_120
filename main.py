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


@login_manager.user_loader
def load_user(user_id):
    return db_session.create_session().query(User).get(user_id)


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
        sess = db_session.create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
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
        sess = db_session.create_session()
        if sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пользователь с данной почтой уже есть')
        f = form.picture.data
        f.save(os.path.join(os.getcwd(), f"static/img/avatars/{len(sess.query(User).all()) + 1}.jpg"))
        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            picture=f"{len(sess.query(User).all()) + 1}.jpg"
        )
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
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
        print(category_of_task)
        sess = db_session.create_session()
        task_number = len(sess.query(CLASS_DICT[category_of_task]).all())
        while True:
            random_task = sess.query(CLASS_DICT[category_of_task]).filter(CLASS_DICT[category_of_task].id == random.randint(1, task_number)).first()
            if not (str(current_user.id) in random_task.done_by):
                break
        return redirect(f"/category_task/{category_of_task}/task/{random_task.id}")


@app.route("/category_task/<int:category>/task/<int:id_task>", methods=["GET", "POST"])
@login_required
def show_task(category, id_task):
    sess = db_session.create_session()
    task = sess.query(CLASS_DICT[category]).get(id_task)
    # print(task.text_of_the_task)
    if request.method == "GET":
        return render_template("task.html", title=f"Задание {category}.{id_task}", task=task, category=category)
    elif request.method == "POST":
        if "answer" in request.form:
            ans = set(request.form["answer"].replace(" ", ""))
            if not (ans == set(task.answers)):
                return render_template("task.html", title=f"Задание {category}.{id_task}",
                                       task=task, category=category, message="Вы ошиблись :(", is_right=-1)
            return render_template("task.html", title=f"Задание {category}.{id_task}",
                                   task=task, category=category, message="Вы ответили верно!", is_right=1)
        return render_template("task.html", title=f"Задание {category}.{id_task}",
                               task=task, category=category, message="Вы ошиблись :(", is_right=-1, is_hint=True)


def main():
    db_session.global_init("db/ege_russian_project.db")
    app.run()


if __name__ == '__main__':
    main()