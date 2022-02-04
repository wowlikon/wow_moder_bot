import requests, io 
from os import *

url = "https://github.com/wowlikon/wow_moder_bot/blob/master/"
files = ("wow_moder_bot.py", "config.py", "filter.py", "requirements.txt")
directory = getcwd()

for file in files:
    filename = str(directory + '\\' + file)
    r = requests.get(url + file)
    with io.open(filename, 'w+') as a:
        a.write(str(r.content))

with io.open("requirements.txt", 'r') as i:
    for line in i.read().splitlines():
        system("pip install " + line)
        system("cls")

mkdir("data")