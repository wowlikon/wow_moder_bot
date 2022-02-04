#Import modules
import logging, mmap
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as ftm
from hashlib import *
from filter import IsAdminFilter
from PIL import Image
from github import Github
import os, math

#Variables
from config import *
with open("requirements.txt", 'r') as f:
    for line in f.read().splitlines():
        os.system("pip install " + line)
        os.system("cls")

#Functions
def clamp(value, vmin, vmax):
    return max(min(value, vmax), vmin)

def symbol(f: float):
    gradient = '  > ` > . > : > ~> ! >/>r>(> l >1>Z>4>H>9>W>8>$>@'.split('>')
    index = int(clamp(f*len(gradient), 0, len(gradient)-1))
    return gradient[index]

def art(path: str):
    p = Image.open(path)
    (width, height) = p.size
    res = math.ceil(width / 20)
    bic = Image.BICUBIC
    p.resize((width * res, height * res), bic)
    rgb = p.convert('RGB')
    string = ''""
    a = 0
    line = height//20
    for i in range(line):
        string += '.'
        for j in range(20):
            r, g, b = rgb.getpixel((i, j))
            a = (r + g + b)/3
            string += symbol(a/255)
        string += '\n'
    return string

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

#Add filter
dp.filters_factory.bind(IsAdminFilter)

#Commands
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

@dp.message_handler(commands=['id'],commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.delete()
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
    text = message.text.lower().split()
    print(message)
    file_name = hash(str(message.chat.id))
    print(file_name)
    file_name += '.bl'
    cens = open(data_dir + file_name, 'r', encoding='utf-8').read().splitlines()
    if len(message.text) > 100:
        await message.reply("Слишком большое сообщение\!", parse_mode = "MarkdownV2")
        print("Слишком большое сообщение!")
    for word in cens:
        delete = (word in text)
        if delete:
            await message.reply("Добавьте '||'")
        if (delete and not message.entities != []) or len(message.text) > 100:
            await message.delete()
            break

@dp.message_handler(content_types=['photo'])
async def handle_ascii_art(message):
    await message.photo[-1].download(data_dir + 'temp.jpg')
    string = art(data_dir + 'temp.jpg')
    await message.answer(string)

#Run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)