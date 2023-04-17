import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from werkzeug.security import generate_password_hash, check_password_hash

from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup
import sqlite3
from data import db_session
from data.users import User
from data.tasks import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/help', '/start'],
                  ['/registration', '/enter']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def echo(update, context):
    pass


async def start(update, context):
    user = update.effective_user
    global name
    name = user.mention_html()
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Со мной ты сдашь русский на 5 баллов!"
        rf"Войди (/enter) или зарегистрируйся (/registration), чтобы получить доступ.",
        reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text('Привет! Я - бот для подготовки к ЕГЭ по русскому языку. '
                                    'Со мной ты можешь порешать задания тестовой части экзамена.')


db_session.global_init("db/ege_russian_project.db")
client = User()
sess = db_session.create_session()


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
            "Попробуйте другой никнейм:")
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
        f"Спасибо за регистрацию, {context.user_data['nickname']}!")
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
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
            f"Пользователя с никнеймом {update.message.text} не существует!\n"
            "Попробуйте ввести никнейм ещё раз или зарегистрируйтесь, введя команду /registration")
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
            f"Вы успешно вошли!")
        return ConversationHandler.END
    await update.message.reply_text('Неверный логин или пароль, попробуйте войти ещё раз, нажав /enter')
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

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
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.run_polling()


if __name__ == '__main__':
    main()