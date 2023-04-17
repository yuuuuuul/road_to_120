import logging
import random

from data.tasks import Task9, Task15, Task10, Task12, Task13, Task16
from werkzeug.security import generate_password_hash, check_password_hash
from data.users import User
from random import choice
import os
from data import db_session
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup
import sqlite3



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/help'],
                  ['/time_left', '/start_preparation']]

reply_keyboard_tasks = [['/9', '/10', '/12'],
                        ['/13', '/15', '/16']]

reply_keyboard_asking = [['/how_to_ans', '/show_ans', '/fuck_off', '/go_to_all_tasks']]
reply_keyboard_done = [['/next_task', '/fuck_off', '/go_to_all_tasks', '/show_adding']]
reply_keyboard_lose = [['/show_adding', '/fuck_off', '/go_to_all_tasks']]
reply_keyboard_agression = [['/start_preparation']]
reply_keyboard_getting_started = [['/registration', '/stop', '/enter']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_done = ReplyKeyboardMarkup(reply_keyboard_done, one_time_keyboard=False)
markup_lose = ReplyKeyboardMarkup(reply_keyboard_lose, one_time_keyboard=False)
markup_tasks = ReplyKeyboardMarkup(reply_keyboard_tasks, one_time_keyboard=False)
markup_agression = ReplyKeyboardMarkup(reply_keyboard_agression, one_time_keyboard=False)
markup_while_asking = ReplyKeyboardMarkup(reply_keyboard_asking, one_time_keyboard=False)
markup_getting_started = ReplyKeyboardMarkup(reply_keyboard_getting_started, one_time_keyboard=False)

db_session.global_init("db/ege_russian_project.db")
client = User()
sess = db_session.create_session()

async def start(update, context):
    await update.message.reply_html(
        f"Привет! Со мной ты сдашь русский на 5 баллов, но для начала зарегистрируйся (/registration) или войди (/enter)",
        reply_markup=markup_getting_started
        )



async def help_command(update, context):
    await update.message.reply_text('Привет! Я - бот для подготовки к ЕГЭ по русскому языку. '
                                    'Со мной ты можешь порешать задания тестовой части экзамена.')


async def time_left(update, context):
    exam = '2023-05-29'
    n = str(datetime.now().date())
    date_format = "%Y-%m-%d"

    a = datetime.strptime(exam, date_format)
    b = datetime.strptime(n, date_format)

    delta = a - b
    await update.message.reply_text(f'До экзамена осталось {delta.days} дней! Тебе конец!',
                                    reply_markup=markup_agression)


async def start_preparation(update, context):
    try:
        if nickname:
            await update.message.reply_text('Отлично! Какое задание будем тренировать?',
                                            reply_markup=markup_tasks)
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def solve_tasks(update, context):
    right = True
    ans = update.message.text
    print(f'solve_tasks_right', context.user_data["right"])
    if ans.lower() != context.user_data["right"]:
        if len(context.user_data["right"]) == len(ans) == len(set(ans)):
            for i in ans:
                print('i', i)
                if not (i in context.user_data["right"]) or i in 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзфывапролдячсмитьбюэъ':
                    right = False
        else:
            right = False
    sess = db_session.create_session()
    now = sess.query(context.user_data["class"]).filter(
        (context.user_data["class"].id == context.user_data["id"])).first()
    if right:
        done = now.done_by
        print(nickname, "nickname")
        if  (now.done_by == None) or (nickname not in now.done_by):
            await update.message.reply_text(random.choice(['молодец!', 'неплохо)', 'а ты хорош!',
                                                           'правильно!', 'угадал!', 'отлично!',
                                                           'и не поспоришь! верно', 'и это правильный ответ!',
                                                           'а ты умен!', 'браво, маэстро!']), reply_markup=markup_done)
        else:
            print('солв таскс не брехайся райт')
            await update.message.reply_text('не брехайся', reply_markup=markup_done)

        if not done:
            done = ''
        done += nickname
        now.done_by = done
        print('done_by_added')
        sess.commit()
    else:
        if (now.done_by == None) or (nickname not in now.done_by):
            await update.message.reply_text(random.choice(['попробуй еще', 'мимо', 'а если подумать?',
                                                           'давай-ка еще попыточку', 'а вот и нет',
                                                           'не попал', 'к сожалению, в молоко',
                                                           'победа была близка, но ответ неверный', 'нет, но не сдавайся!',
                                                           'в целом, было близко']), reply_markup=markup_while_asking)
        else:
            print('солв таскс не брехайся не райт')
            await update.message.reply_text('не брехайся', reply_markup=markup_done)




async def nine(update, context):
    try:
        if nickname:
            task = '9'
            class_of_task = Task9
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def ten(update, context):
    try:
        if nickname:
            task = '10'
            class_of_task = Task10
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)

async def twelve(update, context):
    try:
        if nickname:
            task = '12'
            class_of_task = Task12
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def thirteen(update, context):
    try:
        if nickname:
            task = '13'
            class_of_task = Task13
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)

async def fifteen(update, context):
    try:
        if nickname:
            task = '15'
            class_of_task = Task15
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def sixteen(update, context):
    try:
        if nickname:
            task = '16'
            class_of_task = Task16
            sess = db_session.create_session()
            unsolved = sess.query(class_of_task).filter(
                (class_of_task.done_by.not_like(f"%{nickname}%")) | (class_of_task.done_by == None)).first()
            if unsolved:
                context.user_data["right"] = unsolved.answers
                context.user_data["class"] = class_of_task
                context.user_data["task"] = task
                context.user_data["id"] = unsolved.id
                context.user_data["adding"] = unsolved.adding
                await update.message.reply_text(unsolved.text_of_the_task, reply_markup=markup_while_asking)
                return 1
            else:
                await update.message.reply_text('задания кончились, иди поспи пж')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def how_to_answer(update, context):
    await update.message.reply_text('все как на экзамене: цифры в любом порядке без пробелов и иных символов', reply_markup=markup_while_asking)


async def show_answer(update, context):
    try:
        if nickname:
            sess = db_session.create_session()
            now = sess.query(context.user_data["class"]).filter(
                (context.user_data["class"].id == context.user_data["id"])).first()
            done = now.done_by
            if not done:
                done = ''
            done += nickname
            now.done_by = done
            sess.commit()
            reply = ['рано сдался! а правильный ответ - ','жалко, что у тебя не получилось. Ответ - ',
                      'ну нельзя же так быстро сдаваться. Ответ - ','в следующий раз пытайся думать чуть дольше. Ответ - ',
                      'правильный ответ - ','а я думал, ты не сдашься. Правильный ответ - ']
            a = random.choice(reply)
            await update.message.reply_text(a + context.user_data["right"], reply_markup=markup_done)
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def exxit(update, context):
    try:
        if nickname:
            await update.message.reply_text('Захочешь еще порешать - заходи!', reply_markup=markup)
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def again(update, context):
    try:
        if nickname:
            list_of_tasks_and_classes = {'15': fifteen(update, context),
                                         '9': nine(update, context),
                                         '10': ten(update, context),
                                         '13': thirteen(update, context),
                                         '16': sixteen(update, context),
                                         '12': twelve(update, context)}
            await list_of_tasks_and_classes[context.user_data["task"]]
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)



async def show_adding(update, context):
    try:
        await update.message.reply_text(f'{context.user_data["adding"]}')
    except Exception as e:
        await update.message.reply_text('Сначала зарегистрируйся или войди',
                                        reply_markup=markup_getting_started)


async def registration(update, context):
    await update.message.reply_text(
        "Привет. Спасибо, что решили воспользоваться нашим ботом!\n"
        "Вы можете прервать регистрацию, послав команду /stop.\n"
        "Введите свой никнейм:")
    return 2
    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.

    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


async def get_nickname_reg(update, context):
    await update.message.reply_text("Введите свой никнейм:")
    return 2


# Добавили словарь user_data в параметры.
async def get_email_reg(update, context):
    if sess.query(User).filter(User.nickname == update.message.text).first():
        await update.message.reply_text(
            f"Пользователь с никнеймом {update.message.text} уже существует!\n"
            "Попробуйте другой никнейм, если вы здесь впервые. Если же вы вспомнили,"
            "что уже встречались со мной, то нажмите /stop, а затем /enter, чтобы войти в существующий аккаунт", reply_markup=markup_getting_started)
        return 1
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(
        f"Введите свой email:")
    return 3


async def get_password_reg(update, context):
    if sess.query(User).filter(User.email == update.message.text).first():
        await update.message.reply_text(
            f"Пользователь с email'ом {update.message.text} уже существует!\n"
            "Попробуйте другой email:")
        return 3
    if '@' not in update.message.text:
        await update.message.reply_text('Некорректный email')
        return 3
    context.user_data['email'] = update.message.text
    await update.message.reply_text(
        f"Придумайте пароль")
    return 4


# Добавили словарь user_data в параметры.
async def get_password_again_reg(update, context):
    context.user_data['password'] = update.message.text
    await update.message.reply_text(
        f"Для подтверждения введите его ещё раз")
    return 5


async def get_finish_reg(update, context):
    if context.user_data['password'] != update.message.text:
        await update.message.reply_text(
            f"Пароли не совпадают! Попробуйте ещё раз")
        return 5
    client.nickname = context.user_data['nickname']
    client.email = context.user_data['email']
    client.hashed_password = generate_password_hash(context.user_data['password'])
    global sess
    sess.add(client)
    sess.commit()
    await update.message.reply_text(
        f"Спасибо за регистрацию, {context.user_data['nickname']}!", reply_markup=markup)
    global nickname
    nickname = context.user_data["nickname"]
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


async def stop(update, context):
    return ConversationHandler.END


async def enter(update, context):
    await update.message.reply_text(
        "Привет. Спасибо, что решили воспользоваться нашим ботом!\n"
        "Вы можете прервать вход, послав команду /stop.\n"
        "Введите свой никнейм:")
    return 1


async def get_nickname_log(update, context):
    if not sess.query(User).filter(User.nickname == update.message.text).first():
        await update.message.reply_text(
            f"Пользователя с никнеймом {update.message.text} нет!\n"
            "Попробуйте зарегистрироваться, если вы здесь впервые: нажмите /stop, а затем /registration. Иначе,"
            "введите никнейм корректно", reply_markup=markup_getting_started)
        return 1
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(
        f"Введите свой пароль:")
    return 2


async def get_password_log(update, context):
    context.user_data['password'] = update.message.text
    await update.message.reply_text(
        f"Введите свой email:")
    return 3


async def get_email_log(update, context):
    global sess
    user = sess.query(User).filter(User.email == update.message.text).first()
    if user and user.check_password(context.user_data['password']):
        await update.message.reply_text(
            f"Вы успешно вошли!", reply_markup=markup)
        global nickname
        nickname = context.user_data["nickname"]
        return ConversationHandler.END
    await update.message.reply_text('Неверный логин или пароль, попробуйте войти ещё раз, нажав /enter')
    return ConversationHandler.END


def main():

    db_session.global_init("db/ege_russian_project.db")
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, solve_tasks)
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('9', nine), CommandHandler('10', ten), CommandHandler('12', twelve),
                      CommandHandler('13', thirteen), CommandHandler('15', fifteen), CommandHandler('16', sixteen)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, solve_tasks)],
            },
        fallbacks=[CommandHandler('stop', stop)]

    )
    conv_handler_reg = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('registration', registration)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nickname_reg)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email_reg)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password_reg)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password_again_reg)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_finish_reg)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    conv_handler_log = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('enter', enter)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nickname_log)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password_log)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email_log)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler_reg)
    application.add_handler(conv_handler_log)

    application.add_handler(conv_handler)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time_left", time_left))
    application.add_handler(CommandHandler("start_preparation", start_preparation))
    application.add_handler(CommandHandler('9', nine))
    application.add_handler(CommandHandler('10', ten))
    application.add_handler(CommandHandler('12', twelve))
    application.add_handler(CommandHandler('13', thirteen))
    application.add_handler(CommandHandler('15', fifteen))
    application.add_handler(CommandHandler('16', sixteen))
    application.add_handler(CommandHandler('how_to_ans', how_to_answer))
    application.add_handler(CommandHandler('show_ans', show_answer))
    application.add_handler(CommandHandler('fuck_off', exxit))
    application.add_handler(CommandHandler('next_task', again))
    application.add_handler(CommandHandler('go_to_all_tasks', start_preparation))
    application.add_handler(CommandHandler('show_adding', show_adding))
    application.run_polling()


if __name__ == '__main__':
    main()
