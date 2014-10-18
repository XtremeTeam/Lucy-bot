#===islucyplugin===
# -*- coding: utf-8 -*-

#   Lucy Plugin
#   def_plugin.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict


defines={}

def handler_def(type, source, parameters):
        groupchat = source[1]
        defines=[]
        DBPATH='settings/'+groupchat+'/define.txt'
        defines = eval(read_file(DBPATH))
        command = parameters.split()[0]
        if command in defines.keys():
                definition = defines[command]
                if len(parameters.strip().split()) == 1:
                        reply(type, source, u'You want me to define it in public or private?')
                elif parameters.split()[1] == 'private':
                        reply('private', source, definition)
                elif parameters.split()[1] == 'public':
                        reply(type, source, definition)
        else:
                reply(type, source, u'No such definition')
                return
                

def handler_defadd(type, source, parameters):
        groupchat = source[1]
        definition = None
        command, space, definition = parameters.partition(' ')
	if not parameters:
		reply(type, source, u'What to add !!!?')
	res=define_work(groupchat, command, definition, 1)
	if res:
		reply(type, source, u'added')
	else:
		reply(type, source, u'impossible')
		
def handler_defdel(type, source, parameters):
        groupchat = source[1]
	if not parameters:
		reply(type, source, u'hmmmm?')
	if parameters=='*':
		parameters='0'
	res=define_work(groupchat, parameters, 1, 2)
	if res:
		reply(type, source, u'removed')
	else:
		reply(type, source, u'Such is not present')
                
def handler_deflist(type, source, parameters):
        groupchat = source[1]
	rep,res=u'',define_work(groupchat, 1, 1, 3)
	if res:
		for phrase in res:
			rep+=phrase+u': '+ res[phrase]+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'There are no user phrases')

		
def define_work(groupchat, command, definition,check):
        DBPATH='settings/'+groupchat+'/define.txt'
        if check_file(groupchat,'define.txt'):
                definedb = eval(read_file(DBPATH))
                if check == 1:
                        if not command in definedb.keys():
                            definedb[command] = command
                            definedb[command] = definition
                            write_file(DBPATH, str(definedb))
                            return 1
                        else:
                            msg(groupchat, u'The definition for this command already exists.')
                            return 1
                elif check == 2:
                        if command == '0':
                                definedb.clear()
                                write_file(DBPATH, str(definedb))
                                return True
                        else:
                                del definedb[command]
                                write_file(DBPATH, str(definedb))
                                return True
                elif check ==3:
                        return definedb
        else:
                return None
                
                
                                
register_command_handler(handler_def, 'def', ['def','en','all'], 20, 'Shows the definition of a word that been previously added to the bot.', 'def KiDo parameters',['def KiDo private'])
register_command_handler(handler_defadd, 'defadd', ['def','en','all'], 0, 'Add a word and it\'s definition to the bot.', 'defadd KiDo is my creator.')
register_command_handler(handler_defdel, 'defdel', ['def','en','all'], 20, 'Delete a word and it\'s definition from the bot.\nYou can write defdel * to remove all the definitions.', 'defdel KiDo')
register_command_handler(handler_deflist, 'deflist', ['def','en','all'], 20, 'Shows all the words and their definitions.', 'deflist')
