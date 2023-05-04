# -*- coding: utf-8 -*-
import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import socket
import ssl
import sys

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'bot_logs.log',
    maxBytes=1000000,
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class Telebot:
    """
    Интерфейс для взаимодействия с API Telegram.

    При инициализации экзамляра принимет telegram-токен бота;
    Имеет следующие публичные методы:
    check_updates() - сделать запрос на получения новых сообщений;
    send_reply(user_id, reply) - отправить ответ поьзователю;
                                 Принимает id пользователя и строку 
                                 с отправляемым ответом.
    """
    HOST = 'api.telegram.org'
    PORT = 443
    UPDATE_URL = ('GET /bot{0}/getUpdates?offset={1}&allowed_updates=["message"] HTTP/1.1\r\n'
                  'Host: api.telegram.org\r\n'
                  'Connection: close\r\n\r\n')
    SEND_URL = ('GET /bot{0}/sendMessage?chat_id={1}&text={2}&reply_markup={3} HTTP/1.1\r\n'
                'Host: api.telegram.org\r\n'
                'Connection: close\r\n\r\n')

    def __init__(self, bot_id, offset=None):
        self.id = bot_id
        self.offset = offset

    def _connect(self, host, port):
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            mysock.connect((host, port))
        except socket.error as err:
            logger.error(err, exc_info=True)
            sys.exit(1)
        context = ssl.create_default_context()
        return context.wrap_socket(mysock, server_hostname=host)

    def _make_request(self, cmd):
        mysock = self._connect(self.HOST, self.PORT)
        try:
            mysock.send(cmd.encode('utf-8'))
        except socket.error as err:
            logger.error(err, exc_info=True)
        response = b''
        while True:
            try:
                data = mysock.recv(512)
            except socket.error as err:
                logger.error(err, exc_info=True)
            response += data
            if not data:
                break
        mysock.close()
        return response
    
    def check_updates(self):
        cmd = self.UPDATE_URL.format(self.id, self.offset)
        response = self._make_request(cmd)
        http_response = str(response.decode())
        status = re.match(r'HTTP/1.1 (\d+) (.+)\s', http_response)
        status_code, status_description = status.groups()
        if not 200 <= int(status_code) <= 299:
            error = 'Error: {0} {1}'.format(status_code, status_description)
            logger.error(error)
        pos = http_response.find('\r\n\r\n')
        data_dict = json.loads(http_response[pos:])
        try:
            self.offset = int(data_dict['result'][-1]['update_id']) + 1
        except IndexError:
            pass
        except KeyError:
            pass
        return data_dict

    def send_reply(self, user_id, reply, markup=None):
        markup = markup or ''
        cmd = self.SEND_URL.format(self.id, user_id, reply, markup)
        self._make_request(cmd)
