# encoding: utf-8
__author__ = 'Hukka'


def command_start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I'm maukuBot v0.1.0")   

