#Import modules
import logging, mmap, os, math, time
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as ftm
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import code, italic, bold, pre
from aiogram.utils.markdown import text as my_font
from aiogram.types.message import ContentType
from hashlib import *
from filter import IsAdminFilter
from PIL import Image
from random import choice, randint
from key import *

#Variables
from config import *
times = dict()
rep = dict()
to = 0

#Functions
def exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

def hash(string: str):
    hash = sha1(string.strip().encode('utf-8')).hexdigest()
    return hash

#Bot init
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#Add admin filter
dp.filters_factory.bind(IsAdminFilter)

#Commands
inline_btn_1 = types.InlineKeyboardButton('Пожаловаться!', callback_data='data')
inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)

@dp.message_handler(commands=['report'], commands_prefix='!/')
async def process_command_1(message: types.Message):
    count = await message.chat.get_member_count()
    if message.reply_to_message:
        rep_us = "Пожаловаться на " + message.reply_to_message.from_user["first_name"]
        data =  str(message.chat.id) + 's' + str(message.reply_to_message.from_user.id) + 's' + str(count)
        
        inline_kb1 = types.InlineKeyboardMarkup()
        inline_kb1.add(types.InlineKeyboardButton('Пожаловаться!', callback_data = str(data)))
        await message.reply(rep_us, reply_markup = inline_kb1)
    else:
        await message.reply("Жалоба работает только как ответ")

@dp.callback_query_handler()
async def process_callback_button1(callback: types.CallbackQuery):
    data_en = callback.data.split('s')[:2]
    count = int(callback.data.split('s')[2])
    try:
        rp = rep[str(data_en)]
    except:
        rp = 0
        rep[str(data_en)] = 0
    if rp <= count/2:
        rep[str(data_en)] += 1
        print(rep)
    else:
        print("ban: ", data_en[1])
        await bot.send_message(data_en[0], "BAN")
    await bot.send_message(callback.from_user.id, 'Жалоба отправлена!')

@dp.message_handler(commands=['rand', 'random'], commands_prefix='!/')
async def random(message: types.Message):
    await message.delete()
    r = '.'
    if len(message.text.split()) > 1:
        if message.text.split()[1] == 'map':
            r = choice(map)
        elif message.text.split()[1] == 'cube':
            r = choice(cube)
    else:
        r = randint(0, 10)
    await message.answer(r)

@dp.message_handler(commands=['message_to'], commands_prefix='!/')
async def message_to(message: types.Message):
    text = message.text.split()
    print(text)
    to = text[1]
    mes = text[2:]
    await message.delete()
    await bot.send_message(to, mes)

@dp.message_handler(commands=['start'], commands_prefix='!/')
async def random(message: types.Message):
    await message.delete()
    for mes in name:
        await message.answer(mes)
    await message.answer(help)

@dp.message_handler(commands=['help'], commands_prefix='!/')
async def random(message: types.Message):
    await message.delete()
    await message.answer(help)

@dp.message_handler(commands = ['bl'], commands_prefix = '!/')
async def cmd_bl(message: types.Message):
    texte = message.text.lower()
    file_name = hash(str(message.chat.id))
    print(file_name)
    file_name += '.bl'
    ex = exists(data_dir + file_name)
    if not ex:
        with open(data_dir + file_name, 'w+', encoding='utf-8') as a:
            a.write(' ')
    await message.delete()
    if len(texte.split()) >=2:
        type = texte.split()[1]
    if len(texte.split()) >= 3:
        text = texte.lower().split()[2:]
        text_str = " ".join(text)
        if type == "add":
             await message.answer("added")
             with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                 t = r.read()
             with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                 w.write(text_str + '\n' + t)
        elif type == "delete":
            await message.answer("deleted")
            with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                t = r.read()
            with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                w.write(t.replace(text_str + '\n', ''))
        else:
            await message.answer("Управление блэклистом:\n*добавить солво: !BL add [слово]\n*удалить солово: !BL delete[слово]\n*удалить все солва :!BL clear\n*список запрещёных слов: !BL list")
    else:
        if type == "clear":
            with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                w.close()
            await message.answer("cleared")
        elif type == "list":
            with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                t = r.read()
            await message.answer(t)
        else:
            await message.answer("Управление блэклистом:\n*добавить солво: !BL add [слово]\n*удалить солово: !BL delete[слово]\n*удалить все солва :!BL clear\n*список запрещёных слов: !BL list")

@dp.message_handler(commands=['spam'], commands_prefix = '!/')
async def cmd_spam(message: types.Message):
    if len(message.text.split()) >= 3:
        count = int(message.text.split()[1])
        text = message.text.split()[2:]
        text_str = " ".join(text)
        print("[spamed]" + str(count) + " - \"" + text_str + "\"")
        await message.delete()
        if count <= 25:
            for i in range(count):
                await message.answer(text_str)
        else:
            await message.answer("Не спамь много!")
    else:
        await message.answer("!spam [кол-во] [текст]")

@dp.message_handler(commands=['chat_id'],commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.delete()
    await bot.send_message(message.from_user.id, message.chat.id)

@dp.message_handler(commands=['id'],commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.delete()
    if message.reply_to_message:
        await bot.send_message(message.from_user.id, "User\'s ID: " + str(message.reply_to_message.from_user.id)) 
    else:
        await bot.send_message(message.from_user.id, "You\'re ID: " + str(message.from_user.id))

@dp.message_handler(commands=['echo'], commands_prefix = '!/')
async def cmd_echo(message: types.Message):
    text = message.text.split()[1:]
    text_str = " ".join(text)
    print(text)
    print(text_str)
    await message.delete()
    await message.answer(text_str)

@dp.message_handler(content_types = ["new_chat_members"])
async def on_user_joined(message: types.Message):
    print(message)
    await message.delete()
    user = message.new_chat_members
    bot = user[0]["is_bot"]
    if not bot:
        await message.answer("Добро пожаловать в чат " + str(message.chat.title) + ", " + user[0]["first_name"])

@dp.message_handler(is_admin = True, commands = ["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Это команда работает только как ответ!")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.kick_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(
        ftm.text(
            ftm.text(ftm.hboild("Вам бан")),
            ftm.text(ftm.hunderline("/n от Админа")),
            sep = "\n"), parse_mode = "HTML")

@dp.message_handler()
async def filter_message(message: types.Message):
    global to
    to = to
    t2 = time.time()
    try:
        t1 = times[str(message.from_user.id)]
    except:
        t1 = 2<<15
    times[str(message.from_user.id)] = time.time()
    dt = abs(t1 - t2)
    print(dt)
    if dt <= 0.75:
        await message.delete()
        if abs(to - time.time()) > 5:
            rep = my_font(italic(bold("Не спамь")))
            await message.answer(rep, parse_mode=types.ParseMode.MARKDOWN)
            to = time.time()
    text = message.text.lower().split()
    print(message)
    file_name = hash(str(message.chat.id))
    print(file_name)
    file_name += '.bl'
    cens = open(data_dir + file_name, 'r', encoding='utf-8').read().splitlines()
    if len(message.text) > 150:
        rep = my_font(italic("Слишком большое сообщение"))
        await message.reply(rep, parse_mode = types.ParseMode.MARKDOWN)
        print("Слишком большое сообщение!")
    for word in cens:
        delete = (word in text)
        if delete:
            rep = my_font(italic("Добавьте ll"))
            await message.reply(rep, parse_mode=types.ParseMode.MARKDOWN)
        if (delete and not message.entities != []) or len(message.text) > 100:
            await message.delete()
            break

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    global to
    to = to
    t2 = time.time()
    try:
        t1 = times[str(message.from_user.id)]
    except:
        t1 = 2<<15
    times[str(message.from_user.id)] = time.time()
    dt = abs(t1 - t2)
    print(dt)
    if dt <= 0.75:
        await message.delete()
        if abs(to - time.time()) > 5:
            rep = my_font(italic(bold("Не спамь")))
            await message.answer(rep, parse_mode=types.ParseMode.MARKDOWN)
            to = time.time()
    print(message)


#Run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)