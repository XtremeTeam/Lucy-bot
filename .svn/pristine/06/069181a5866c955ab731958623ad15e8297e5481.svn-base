#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  query_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_query_get_public(type, source, parameters):
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of  bot')
		return
	if parameters:
		if localdb.has_key(string.lower(parameters)):
			reply(type, source, u'About <' + parameters + u'> I know the following:\n' + localdb[string.lower(parameters)])
		else:
			reply(type, source, u'I dont know <' + parameters + '> :(')
	else:
			reply(type, source, u'hmmmm?')

def handler_query_get_private(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'Mistake at creating base. Tell about it to the administrator of a bot')
		return
	tojid = ''
	rep = u'кому?'
	localdb = eval(read_file(DBPATH))
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if get_bot_nick(groupchat) != nick:
				if nick in nicks:
					tojid = groupchat+'/'+nick
		else:
			tojid = groupchat+'/'+source[2]
			body = parameters
	if tojid:
		if localdb.has_key(string.lower(body)):
			if type == 'public':
				reply(type, source, u'Cunningly')
			msg(tojid, u'about <' + body + u'> I know the following:\n\n'+localdb[string.lower(body)])
		else:
			reply(type, source, u'I dont know  <' + body + '> :(')
	else:
		reply(type, source, u'To whom?')

		
def handler_query_get_random(type, source, parameters):
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of a bot')
		return
	if not localdb.keys():
		reply(type, source, u'The base is empty!')
		return
	rep = random.choice(localdb.keys())
	reply(type, source, u'About <' + rep + u'> I know the following:\n' + localdb[rep])


def handler_query_set(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		keyval = string.split(parameters, '=', 1)
		if not len(keyval)<2:
			key = string.lower(keyval[0]).strip()
			value = keyval[1].strip()
			if not value:
				if localdb.has_key(key):
					del localdb[key]
				reply(type, source, key + u' -> прибил нафиг')
			else:
				localdb[key] = keyval[1].strip()+u' (from '+source[2]+')'
				reply(type, source, u'Now I shall know, What is ' + key)
			write_file(DBPATH, str(localdb))
		else:
			reply(type, source, u'hmmmm?')
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of a bot')

def handler_query_count(type, source, parameters):
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=str(len(localdb.keys()))
		reply(type, source, 'In base of answers/questions given конфы '+num+' Records')
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of a bot')
		return

def handler_query_search(type, source, parameters):
	if not parameters:
		reply(type, source, u'hmmmm?')
		return
	rep=[]
	groupchat=source[1]	
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		if not localdb.keys():
			reply(type, source, u'The base is empty!')
			return
		for x in localdb:
			if x.count(parameters)>0:
				rep.append(x)
		if rep:
			reply(type,source,u'Has coincided с:\n'+', '.join(rep))
		else:
			reply(type,source,u'With what has not coincided :(')
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of a bot')
		return
		
def handler_query_all(type, source, parameters):
	groupchat=source[1]
	DBPATH='settings/'+groupchat+'/localdb.txt'
	if check_file(groupchat,'localdb.txt'):
		localdb = eval(read_file(DBPATH))
		num=len(localdb.keys())
		if num == 0:
			reply(type, source, 'The base is empty!')
			return
		reply(type, source, ', '.join(localdb.keys()))
	else:
		reply(type,source,u'Mistake at creation of base. Tell about it to the administrator of a bot')
		return


register_command_handler(handler_query_get_public, '!', ['info','wtf','all'], 10, 'Searches for the answer to a question in local base (analogue wtf in сульцах).', '?? <Inquiry>', ['?? something', '?? Something'])
register_command_handler(handler_query_get_private, '!?', ['info','wtf','all'], 10, 'Searches for the answer to a question in local base and sends it in private (analogue! for private).', '!?? <nick> <query>', ['!? something', '!? guy something'])
register_command_handler(handler_query_set, '!!', ['info','wtf','admin','all'], 11, 'Establishes the answer to a question in local base (analogue dfn in сульцах).', '!!! <Inquiry> = <The answer>', ['!! something = the best!', '!! something else ='])
register_command_handler(handler_query_count, '?count', ['info','wtf','all'], 10, 'Shows quantity of questions in base конфы (analogue wtfcount in сульцах).', '!!! ???count', ['???count'])
register_command_handler(handler_query_get_random, '??rand', ['info','wtf','all'], 10, 'Shows casually chosen answer to a question (analogue wtfrand in сульцах).', '???rand', ['???rand'])
register_command_handler(handler_query_search, '??search', ['info','wtf','all'], 10, 'search for an inquiry in base.', '???search <Inquiry>', ['???search something'])
register_command_handler(handler_query_all, '??all', ['info','wtf','all'], 10, 'Shows all keys of base (cautiously, can be much!).', '???all', ['???all'])
