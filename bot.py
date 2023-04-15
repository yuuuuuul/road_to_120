import logging
from data.tasks import Task9, Task15, Task10, Task12, Task13, Task16
from data.users import User
import os
from data import db_session
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup
import sqlite3




name = ''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/help'],
                  ['/time_left', '/start_preparation']]

reply_keyboard_tasks = [['/9', '/10', '/12'],
                        ['/13', '/15', '/16']]

reply_keyboard_asking = [['/how_to_ans', '/show_ans', '/fuck_off', '/go_to_all_tasks']]
reply_keyboard_done = [['/next_task', '/fuck_off', '/go_to_all_tasks']]
reply_keyboard_lose = [['/show_adding', '/fuck_off', '/go_to_all_tasks']]
reply_keyboard_agression = [['/start_preparation']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_done = ReplyKeyboardMarkup(reply_keyboard_done, one_time_keyboard=False)
markup_lose = ReplyKeyboardMarkup(reply_keyboard_lose, one_time_keyboard=False)
markup_tasks = ReplyKeyboardMarkup(reply_keyboard_tasks, one_time_keyboard=False)
markup_agression = ReplyKeyboardMarkup(reply_keyboard_agression, one_time_keyboard=False)
markup_while_asking = ReplyKeyboardMarkup(reply_keyboard_asking, one_time_keyboard=False)


"""async def echo(update, context):
    if update.message.text[0] in '1234567890':
        context.user_data["ans"] = update.message.text
        #print(context.user_data)"""


async def start(update, context):
    user = update.effective_user
    global name
    name = user.mention_html()
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Со мной ты сдашь русский на 5 баллов!",
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


async def solve_tasks(update, context):
    right = True
    ans = update.message.text
    print(f'solve_tasks_right', context.user_data["right"])
    if ans != context.user_data["right"]:
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
        if  (now.done_by == None) or ('lalala' not in now.done_by):
            await update.message.reply_text('молодец!', reply_markup=markup_done)
        else:
            await update.message.reply_text('не брехайся', reply_markup=markup_done)
        if not done:
            done = ''
        done += 'lalala'
        now.done_by = done
        print('done_by_added')
        sess.commit()
    else:
        if (now.done_by == None) or ('lalala' not in now.done_by):
            await update.message.reply_text('попробуй еще', reply_markup=markup_while_asking)
        else:
            await update.message.reply_text('не брехайся', reply_markup=markup_done)




async def nine(update, context):
    task = '9'
    class_of_task = Task9
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter(
        (class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def ten(update, context):
    task = '10'
    class_of_task = Task10
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter(
        (class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def twelve(update, context):
    task = '12'
    class_of_task = Task12
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter(
        (class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def thirteen(update, context):
    task = '13'
    class_of_task = Task13
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter(
        (class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def fifteen(update, context):
    task = '15'
    class_of_task = Task15
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter((class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def sixteen(update, context):
    task = '16'
    class_of_task = Task16
    sess = db_session.create_session()
    unsolved = sess.query(class_of_task).filter(
        (class_of_task.done_by.not_like("%lalala%")) | (class_of_task.done_by == None)).first()
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


async def how_to_answer(update, context):
    await update.message.reply_text('все как на экзамене: цифры в любом порядке без пробелов и иных символов', reply_markup=markup_while_asking)


async def show_answer(update, context):
    sess = db_session.create_session()
    now = sess.query(context.user_data["class"]).filter(
        (context.user_data["class"].id == context.user_data["id"])).first()
    done = now.done_by
    if not done:
        done = ''
    done += 'lalala'
    now.done_by = done
    sess.commit()
    await update.message.reply_text(f'рано сдался! а правильный ответ: {context.user_data["right"]}', reply_markup=markup_done)


async def exxit(update, context):
    await update.message.reply_text('Захочешь еще порешать - заходи!', reply_markup=markup)


async def again(update, context):
    list_of_tasks_and_classes = {'15': fifteen(update, context),
                                 '9': nine(update, context),
                                 '10': ten(update, context),
                                 '13': thirteen(update, context),
                                 '16': sixteen(update, context),
                                 '12': twelve(update, context)}
    await list_of_tasks_and_classes[context.user_data["task"]]


async def show_adding(update, context):
    await update.message.reply_text(f'{context.user_data["adding"]}')


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
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

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

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
