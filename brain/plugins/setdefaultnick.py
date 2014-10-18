#===islucyplugin===
# -*- coding: utf-8 -*-
#   setdefaultnick_plugin.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

def handler_default_bot_nick(type, source, parameters):
        add_gch(source[1], DEFAULT_NICK)
        join_groupchat(source[1], DEFAULT_NICK)
        reply(type, source, u'OK, the default nickname has been set.')

register_command_handler(handler_default_bot_nick, 'sdbn', ['delirium','en','all'], 20, 'Change the nickname of the bot to it\'s default, which is '+DEFAULT_NICK, 'sdbn')
