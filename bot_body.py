from pathlib import Path
import time
import logging
import json
from aiogram import Bot, types, Dispatcher, executor
import asyncio

user_dir = 'users.txt'
message_dir = 'message.txt'
API_TOKEN = ''
message_obj = None
user_obj = None
success_action = []

# Отсутствие обфускации - указание автора
# No obfuscation - author's indication

with open('token.json', 'r') as token_file:
    API_TOKEN = json.load(token_file)["token"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
abs_path = Path().absolute()

def get_message():
    global message_obj
    global abs_path
    if Path(str(abs_path) + '\\' + message_dir).exists():
        with open(message_dir, encoding="utf-8") as m_file:
            message_obj = m_file.read()
            if message_obj == None:
                return print("Error: message text is empty")
            else:
                get_users()
    else:
        Path(str(abs_path) + '\\' + message_dir).parent.mkdir(parents=True, exist_ok=True)
        file = open(message_dir, 'w')
        file.write("Your text goes here")
        file.close()
        return print("Error: message dir is not exist")

def get_users():
    global message_obj
    global abs_path
    global user_obj
    if Path(str(abs_path) + '\\' + user_dir).exists():
        if message_obj is not None:
            with open(user_dir, encoding="utf-8") as u_file:
                data = u_file.readlines()
                if data is not None:
                    users = [x.strip() for x in data]
                    if users != []:
                        user_obj = users
                    else:
                        return print("Error: userlist is empty")
                else:
                    return print("Error: broken userlist file")
        else:
            return print("Error: message_obj == null is true")
    else:
        Path(str(abs_path) + '\\' + user_dir).parent.mkdir(parents=True, exist_ok=True)
        file = open(user_dir, 'w')
        file.write("user_id\nuser_id")
        file.close()
        return print("Error: userdir is not exist")

async def send_message(index):
    global message_obj
    global user_obj
    global success_action
    global bot
    try:
        await bot.send_message(chat_id=user_obj[index], text=message_obj)
        success_action.append(user_obj[index])
    except:
        None

def create_tasks(loop):
    global user_obj
    tasks = [loop.create_task(send_message(i)) for i in range(0, len(user_obj))]
    return tasks

def result_func():
    global user_obj
    global success_action
    if len(user_obj) != len(success_action):
        for i in user_obj:
            if not success_action.__contains__(i):
                print("Result: user with id '{}' didn't receive message".format(i))
    else:
        print("Result: mailing is over with success")

async def bot_stop():
    global bot
    await bot.close()

if __name__ == '__main__':
    get_message()
    if message_obj is not None and user_obj is not None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(create_tasks(loop)))
        loop.run_until_complete(bot_stop())
        loop.close()
        result_func()
    else:
        print("Error: files")