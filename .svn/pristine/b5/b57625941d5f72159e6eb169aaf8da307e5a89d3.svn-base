#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  turn_plugin.py

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

global_en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,./`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,./`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~"))

turn_msgs={}

def handler_turn_last(type, source, parameters):
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)	
	if parameters:
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),parameters))
	else:
		if turn_msgs[groupchat][jid] is None:
			reply(type,source,u' And you still did not say anything!')
			return

		if turn_msgs[groupchat][jid] == u'%sturn' % (COMM_PREFIX):
			reply(type,source,u'А вот фиг!')
			return
		
		tmsg=turn_msgs[groupchat][jid]
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),tmsg))

def handler_turn_save_msg(type, source, body):
	time.sleep(1)
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)
	if groupchat in turn_msgs.keys():
		if jid in turn_msgs[groupchat].keys() and jid != groupchat and jid != JID:
			turn_msgs[groupchat][jid]=body
	
def handler_turn_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if not groupchat in turn_msgs.keys():
		turn_msgs[groupchat] = {}
	if not jid in turn_msgs[groupchat].keys() and jid != JID:
		turn_msgs[groupchat][jid]=None

register_message_handler(handler_turn_save_msg)
register_join_handler(handler_turn_join)

register_command_handler(handler_turn_last, COMM_PREFIX+'turn', ['muc','all','*'], 10, 'Switch layout for the last message for the user of causing command.', COMM_PREFIX+'turn', [COMM_PREFIX+'turn'])