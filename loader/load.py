from telethon import TelegramClient
from telethon import events, utils
import telethon
import configparser
import os

config = configparser.ConfigParser()
config.read('loader/config.ini')
api_id = int(config.get('API', 'API_id'))
api_hash = config.get('API', 'API_hash')
if os.path.exists("loader/account/user.session"):
    class TGclient:
        client = TelegramClient('loader/account/user.session', api_id, api_hash)
        ct = 1
else:
    class TGclient:
        client = TelegramClient('loader/user.session', api_id, api_hash)
        ct = 1
    