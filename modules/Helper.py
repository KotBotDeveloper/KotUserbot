from telethon import TelegramClient
from telethon import events, utils
from loader.load import *
import os
import requests
import shutil
import asyncio
from time import sleep
import importlib
clientTG = TGclient()
client = clientTG.client

@client.on(events.NewMessage(pattern='!info'))
async def helps(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.delete()
        
        folder_path = "modules"
        file_names_without_extension = []
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            if file_name != "__pycache__":
                name_without_extension = os.path.splitext(file_name)[0]
                file_names_without_extension.append(name_without_extension)
            modul = "\n".join(file_names_without_extension)
        await event.reply(f"KotUserbot v0.1.2\nК вашим услугам.\nВот ваши установленные модули:\n{modul}")


@client.on(events.NewMessage(pattern='!help'))
async def helps(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.delete()
        await event.reply("Здравствуйте, вот список команд:\n!del (Имя модуля) - удаляет модуль,\n!install (ссылка) - установка модуля,\n!(имя модуля) - позволяет узнать информацию о модуле\n!info - Позволяет узнать какие модули установленны")
