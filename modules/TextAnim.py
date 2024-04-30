from telethon import TelegramClient
from telethon import events, utils
from loader.load import *
import importlib
import asyncio

clientTG = TGclient()
client = clientTG.client
type_symbol = "|"

@client.on(events.NewMessage(pattern=r'!TextAnim'))
async def textanim_message(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit("Модуль TextAnim\n!type(Текст) - Анимация текста\n!type_symbol (символ) - изменение символа для анимации")
        
@client.on(events.NewMessage(pattern=r'!type_symbol(.+)'))
async def type_editmessage(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        global type_symbol
        type_symbol = event.pattern_match.group(1)
        await event.edit("Настройки измененны !")
        
@client.on(events.NewMessage(pattern=r'!type (.+)'))
async def type_message(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        input_text = event.pattern_match.group(1)
        temp_text = input_text
        edited_text = ""
        typing_symbol = type_symbol

        while edited_text != input_text:
            try:
                await event.edit(edited_text + typing_symbol)
                await asyncio.sleep(0.05)
                edited_text = edited_text + temp_text[0]
                temp_text = temp_text[1:]
                await event.edit(edited_text)
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Ошибка: {e}")
        