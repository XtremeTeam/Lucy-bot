#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's plugin

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>

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
			reply(type,source,u'you said nothing')
			return
		if turn_msgs[groupchat][jid] == u'turn':
			reply(type,source,u'not allowed')
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

def handler_correct_message(type, source, parameters):
        groupchat = source[1]
        nick = source[2]
        jid = get_true_jid(groupchat+'/'+nick)
        wword, seperator, rword = parameters.partition(' ')
        message = ''
        words = ''
        wmessage = turn_msgs[groupchat][jid].strip().split()
        if not wword in wmessage:
                reply(type, source, u'No such word')
                return
        for i in range(0, len(wmessage)):
                       if wword == wmessage[i]:
                               message += rword
                               message += ' '
                       else:
                               message += wmessage[i]
                               message += ' '
        msg(groupchat, nick+u' meant to say:\n'+message)
        return
        
register_message_handler(handler_turn_save_msg)
register_join_handler(handler_turn_join)
register_command_handler(handler_turn_last, 'turn', ['turn','en','all'], 100, 'Commutes the lay-out of keyboard for the latest report from the user of causing command.', 'turn', ['turn'])
register_command_handler(handler_correct_message, 'correct', ['turn','en','all'], 0, 'Type correct followed by the wrong and the right words in order to correct the last sentence.','correct wrong-word right-word',['hello gays'],['correct gays guys'])

