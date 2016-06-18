#!/usr/bin/env python
# encoding: utf-8

__author__ = 'pikkuhukka@gmail.com'

import logging
import os
import time
from telegram import (Updater, Dispatcher)
from config import *

updater = Updater(token=TG_TOKEN)

class PyteBot(object):

    module_directory = os.path.join(os.getcwd(), "modules")

    def __init__(self, dispatcher, log):
        """
        :type dispatcher: Dispatcher
        :return:
        """
        self.dispatcher = dispatcher
        self.log = log
        self.module_namespace = {}
        self.started_at = time.time()
        self._load_modules()
        self._register_handlers()

    def _add_message_handler(self, handler):
        self.dispatcher.addTelegramMessageHandler(handler)

    def _add_command_handler(self, command_name, handler):
        self.dispatcher.addTelegramCommandHandler(command_name, handler)

    def _add_regex_handler(self, matcher, handler):
        self.dispatcher.addTelegramRegexHandler(matcher, handler)

    def _load_modules(self):
        for module in self._get_all_modules():
            self.log.info("Loading module %s" % module)
            _ns = {}
            execfile(os.path.join(self.module_directory, module), _ns, _ns)
            if 'boot' in _ns:
                _ns['init'](self)
            self.module_namespace[module] = (_ns, _ns)

    def _register_handlers(self):
        for module, _ns in self.module_namespace.items():
            globals, locals = _ns
            l_items = locals.items()
            for cmd, ref in l_items:
                if cmd.startswith('command_'):
                    print "-- Adding command handler: %s %s --" % (self._get_id(cmd), ref) 
                    self._add_command_handler(self._get_id(cmd), ref)
                elif cmd.startswith('matcher_'):
                    # ref is the regex
                    re_cmd = 'regex_' + self._get_id(cmd)
                    handler = [l for l in l_items if l[0] == re_cmd][0]
                    if handler:
                        print "-- Adding regex handler: %s %s %s --" % (handler[0], ref, handler[1])
                        self._add_regex_handler(ref, handler[1])
                elif cmd.startswith('message_'):
                    print "-- Adding message handler: %s %s --" % (cmd, ref)
                    self._add_message_handler(ref)

    
    def _get_id(self, cmd):
        return '_'.join(cmd.split("_")[1:])

    def _get_all_modules(self):
        return [f for f in os.listdir(self.module_directory) if f.startswith("module_") and f.endswith(".py")]


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log = logging.getLogger('pytebot')
    dispatcher = updater.dispatcher
    print "-- Starting PyteBot --"
    bot = PyteBot(dispatcher, log)
    updater.start_polling()


if __name__ == '__main__':
    main()
