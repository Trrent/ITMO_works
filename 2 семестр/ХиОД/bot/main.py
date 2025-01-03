import logging
import os
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import filters
from random import choice

from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv

from data.tasks import Task
from data.users import User
from data.reports import Report
from data import db_session

load_dotenv(find_dotenv())

task_buttons = {4: '4️⃣',
                # 7: '7️⃣',
                8: '8️⃣',
                # 9: '9️⃣',
                # 10: '🔟',
                # 11: '1️⃣1️⃣',
                # 12: '1️⃣2️⃣',
                '4️⃣': 4,
                # '7️⃣': 7
                '8️⃣': 8}
# '9️⃣': 9,
# '🔟': 10,
# '1️⃣1️⃣': 11,
# '1️⃣2️⃣': 12}

TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
MY_ID = os.environ.get('MY_ID')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}')
    get_user(message.from_user)
    await send_menu(message=message)


@dp.poll_answer_handler()
async def poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    try:
        user = get_user(poll_answer.user)
        if user.task_id:
            add_report(user_id, user.task_id, is_right_answer(user.task_id, poll_answer.option_ids[0]))
            await send_poll(poll_answer.user, get_task(user.task_id).type)
        else:
            await send_menu(types.Message(), user_id=user_id)
    except Exception as e:
        await exception_handler(e, user_id)


@dp.message_handler(filters.Text(equals=task_buttons.values()))
async def poll(message: types.Message):
    user_id = message.from_user.id
    try:
        user = get_user(message.from_user)
        user.task_type = task_buttons[message.text]
        session.commit()
        await send_poll(message.from_user, task_buttons[message.text])
    except Exception as e:
        await exception_handler(e, user_id)


async def send_poll(user_data, task_type):
    task = None
    explanation = None
    try:
        user = get_user(user_data)
        tasks = get_tasks(task_type)
        task = choice(tasks)
        user.task_id = task.id
        options = task.options.split('%')
        correct_option = task.correct_option
        if task.rule:
            explanation = '\n'.join(task.rule.rule.split('\\n'))
        await bot.send_poll(chat_id=user.user_id,
                            question=task.question,
                            options=options,
                            type='quiz',
                            explanation=explanation,
                            correct_option_id=options.index(correct_option),
                            is_anonymous=False,
                            reply_markup=types.ReplyKeyboardRemove())
        session.commit()
    except Exception as e:
        await exception_handler(e, user_data.id, task)


@dp.message_handler(commands=['menu', 'stop', 'help'])
async def send_menu(message: types.Message, user_id=None):
    if not user_id:
        user_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row(types.KeyboardButton(task_buttons[4]), types.KeyboardButton(task_buttons[8]))
    await bot.send_message(chat_id=user_id,
                           text='Выберите тип задания для тренировки\n\nДля остановки используйте /stop',
                           reply_markup=keyboard)


def get_user(user_data):
    user = session.query(User).filter(User.user_id == user_data.id).first()
    if not user:
        user = User(user_id=user_data.id, username=user_data.username, user_first_name=user_data.first_name)
        session.add(user)
        session.commit()
        logging.info(f"New user: {user_data.id}")
    return user


def get_tasks(task_type):
    return session.query(Task).filter(Task.type == task_type).all()


def get_task(task_id):
    return session.query(Task).filter(Task.id == task_id).first()


def add_report(user_id, task_id, answer):
    report = Report(user_id=user_id, task_id=task_id, is_right_answer=answer)
    session.add(report)
    session.commit()
    return report


def is_right_answer(task_id, option):
    task = session.query(Task).filter(Task.id == task_id).first()
    option = task.options.split('%')[option]
    return task.correct_option == option


async def exception_handler(exception_text, user_id, task=None):
    logging.error(f"Exception: {exception_text}")
    await bot.send_message(chat_id=MY_ID, text=exception_text)
    if task:
        await bot.send_message(chat_id=MY_ID, text=str(task.id))


@dp.message_handler()
async def non(message: types.Message):
    await message.answer('Эта команда мне неизвестна:(')


if __name__ == '__main__':
    db_session.global_init(os.sep.join([os.path.abspath(os.path.dirname(__file__)), "db", "ege.db"]))
    session = db_session.create_session()
    executor.start_polling(dp)
