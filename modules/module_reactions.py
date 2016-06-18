__author__ = 'Hukka'

import json

matcher_alkukork = "^[\s\S]{0,1}kork"
matcher_loppukork = "[\s]kork[\s\S]{0,1}$"

def command_kork(bot, update, args):
    """korkkaa kalian"""
    user = update.message.from_user.username
    if args:
        drink = ' '.join(args)
        bot.sendMessage(chat_id=update.message.chat_id, text="@%s *%s-KORK* *tshhhhh* *glug*glug*glug*glug* *aaaaaaah*" % (user, drink))
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="@%s *KORK* *tshhhhh* *glug*glug*glug*glug* *aaaaaaah*" % user)

def regex_alkukork(bot, update, args):
    command_kork(bot, update, args)

def regex_loppukork(bot, update, args):
    command_kork(bot, update, args)

