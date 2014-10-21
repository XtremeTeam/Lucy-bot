#===islucyplugin===
# -*- coding: utf-8 -*-

#   prefix.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

def handler_prefix(type, source, parameters):
        groupchat = source[1]
        DBPATH='settings/chatrooms.list'
        prefixdb = eval(read_file(DBPATH))
        charlist = ['!','@','#','$','%','^','&','*','(',')','_','-','=','+','/',']','[','}','{','"',';',':','|','?','<','>','.',',','~','`']
        if parameters in charlist:
                prefixdb[groupchat]['prefix'] = 'prefix'
                prefixdb[groupchat]['prefix'] = parameters
                write_file(DBPATH, str(prefixdb))
                reply(type, source, u'OK, '+parameters+u' has been set as a prefix.')
        elif parameters.lower() == 'none':
                prefixdb[groupchat]['prefix'] = 'prefix'
                prefixdb[groupchat]['prefix'] = ''
                write_file(DBPATH, str(prefixdb))
                reply(type, source, u'OK, won\'t use any prefix.')               
        elif parameters.lower() == 'list':
                reply(type, source, u'The characters that you can use to set as a prefix are:\n~ ` ! @ # $ % ^ & * ( ) _ - = + | { } [ ] " ; : / < > . , ?')
        elif not parameters:
                if prefixdb[groupchat]['prefix'] == '':
                        reply(type, source, u'No prefix has been set.')
                else:
                        reply(type, source, prefixdb[groupchat]['prefix'])
        elif not parameters in charlist:
                reply(type, source, u'This is not valid prefix, please type prefix list to show you a list of the characters you can use.')

                
register_command_handler(handler_prefix, 'prefix', ['prefix','en','all'], 0, 'Type prefix followed by any character to set as a prefix for the commands.\nType prefix list to see the list of characters that are allowed.\nType prefix none, to remove the prefix.','prefix character',['prefix','prefix list','prefix none','prefix !'])