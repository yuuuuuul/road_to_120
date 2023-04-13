import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup
import sqlite3

name = ''
# Подключение к БД
con = sqlite3.connect("ege_russian_project.sqlite")

# Создание курсора
cur = con.cursor()

# Выполнение запроса и получение всех результатов

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/help'],
                  ['/time_left', '/start_preparation']]

reply_keyboard_tasks = [['/9', '/10', '/12'],
                        ['/13', '/15', '/16']]

reply_keyboard_agression = [['/start_preparation']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_tasks = ReplyKeyboardMarkup(reply_keyboard_tasks, one_time_keyboard=True)
markup_agression = ReplyKeyboardMarkup(reply_keyboard_agression, one_time_keyboard=True)


async def echo(update, context):
    pass


async def start(update, context):
    user = update.effective_user
    global name
    name = user.mention_html()
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Со мной ты сдашь русский на 5 баллов!",
        reply_markup=markup
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
    await update.message.reply_text('Отлично! Какое задание будем тренировать?',
                                    reply_markup=markup_tasks)


async def solve_tasks(update, context, task):
    table_name = f'task_{task}'
    result = cur.execute(f"""SELECT * FROM {table_name}
                WHERE NOT {name} in done_by""").fetchall()
    await update.message.reply_text('rp;98kifug')


async def nine(update, context):
    task = '9'
    await solve_tasks(update, context, task)


async def ten(update, context):
    task = '10'
    await solve_tasks(update, context, task)


async def twelve(update, context):
    task = '12'
    await solve_tasks(update, context, task)


async def thirteen(update, context):
    task = '13'
    await solve_tasks(update, context, task)


async def fifteen(update, context):
    task = '15'
    await solve_tasks(update, context, task)


async def sixteen(update, context):
    task = '16'
    await solve_tasks(update, context, task)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

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
    application.run_polling()


if __name__ == '__main__':
    main()
