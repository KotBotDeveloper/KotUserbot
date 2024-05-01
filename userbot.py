import loader
import os
import configparser
from telethon.errors import ApiIdInvalidError
import sys
import asyncio
from telethon import TelegramClient
from telethon import events, utils
import importlib
import glob
import requests
from time import sleep
import shutil
client = None
from loader.load import TGclient

def login():
    while True:
        res = input("Введите API_ID: ")
        if res.isdigit():
            print("\n\033[47m\033[30mСохраняю данные\033[0m\n")
            break
        else:
            print("В числе содержатся лишние символ\n")
    resid = input("Введите API_HASH: ")
    print("\n\033[47m\033[30mСохраняю данные\033[0m\n")
    
    config = configparser.ConfigParser()
    config.add_section('API')
    config.set('API', 'API_id', f"{res}")
    config.set('API', 'API_hash', f"{resid}")
    with open('loader/config.ini', 'w') as configfile:
        config.write(configfile)
        sleep(1)
    while True:
        try:
            config.read('loader/config.ini')

            api_id = int(res)
            api_hash = resid
            clientTG = TGclient()
            clientTG.client.disconnect()
            clientTG.client = TelegramClient('loader/user.session', api_id, api_hash)
            client = clientTG.client
            client.start()
            print("Вход выполнен!")
            os.replace("loader/user.session", "loader/account/user.session")
            print("Пожалуйста перезапустите программу введя: python userbot.py")
            break
        except ApiIdInvalidError:
            print("\nневерный API_ID или API_HASH, повторите вход ещё раз\n")
            break
            sys.exit()
            


async def started():
    
    global client
    
    module_files = glob.glob("modules/*.py")
    config = configparser.ConfigParser()
    config.read('loader/config.ini')
    api_id = int(config.get('API', 'API_id'))
    api_hash = config.get('API', 'API_hash')
    clientTG = TGclient()
    ct = clientTG.ct
    client = clientTG.client
    if ct == 2:
        await client.disconnect()
    await client.start()
    
    me = await client.get_me()
    ct = 2
    for file in module_files:
        module_name = file.split("/")[-1][:-3]
        try:
            module = importlib.import_module(f"modules.{module_name}")
        except ImportError:
            await client.send_message(me.id, f"Произошла ошибка при импорте модуля: **{module_name}**, возможно модуль не подходит для этого юзербота")
    print("Бот запущен")
    
    @client.on(events.NewMessage(pattern='!del'))
    async def dels(event):
        me = await client.get_me()
        if event.sender_id == me.id:
            await event.delete()
            module_del = event.raw_text.split("!del ")[1]
            moddel = f"modules/{module_del}.py"
            if os.path.exists(moddel):
                os.remove(moddel)
                await event.reply(f"Модуль {module_del} успешно удалён")
                await restart()
            else:
                await event.reply(f"Модуль с именем {module_del} не найден !")
            
            
            
    @client.on(events.NewMessage(pattern='!install'))
    async def helps(event):
        me = await client.get_me()
        if event.sender_id == me.id:
            await event.delete()
            text = event.raw_text.split("!install ")[1]
            response = requests.get(text)
            filename = os.path.basename(text)
            extension = os.path.splitext(filename)
            ex = extension[1]
            if extension[1] != ".py":
                await event.reply("Ошибка: файл не найден или содержит неверный формат")
            else:
                inst = await event.reply(f"Устанавливаю модуль ```{filename}```")
                sleep(1)
            
                with open(filename, "wb") as file:
                    await client.delete_messages(event.chat_id, [inst.id])
                    file.write(response.content)
                    shutil.move(filename, f"modules/{filename}")
                    await event.reply(f"Ваш модуль успешно установлен ! ```{filename}```")
                
                await restart()
    await client.run_until_disconnected()   
    
    
async def restart():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(await started())
    
if os.path.exists("loader/account/user.session"):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(started())
else:
   login()
   
