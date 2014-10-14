#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  upside_plugin.py


# coded by nikk
# exclusive for www.virtualtalk.org
global_en2ru_table = dict(zip(u"abcdefghijklmnopqrstuvwxyzɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎzABCDEFGHIJKLMNOPQRSTUVWXYZ", u"ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎzabcdefghijklmnopqrstuvwxyzɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎzabcdefghijklmnopqrstuvwxyz"))

turn_msgs={}

def handler_upside_last(type, source, parameters):
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)	
	if parameters:
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),parameters))
	else:
		if turn_msgs[groupchat][jid] is None:
			reply(type,source,u'you nothing write')
			return
		if turn_msgs[groupchat][jid] == u'upside':
			reply(type,source,u'forbidden')
			return		
		tmsg=turn_msgs[groupchat][jid]
		reply(type,source,reduce(lambda x,y:global_en2ru_table.get(x,x)+global_en2ru_table.get(y,y),tmsg))

def handler_upside_save_msg(type, source, body):
	time.sleep(1)
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)
	if groupchat in turn_msgs.keys():
		if jid in turn_msgs[groupchat].keys() and jid != groupchat and jid != JID:
			turn_msgs[groupchat][jid]=body
	
def handler_upside_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if not groupchat in turn_msgs.keys():
		turn_msgs[groupchat] = {}
	if not jid in turn_msgs[groupchat].keys() and jid != JID:
		turn_msgs[groupchat][jid]=None


register_message_handler(handler_upside_save_msg)
register_join_handler(handler_upside_join)
register_command_handler(handler_upside_last, COMM_PREFIX+ 'upside', ['all'], 10, 'replace english letters with upside down.', COMM_PREFIX+'upside', ['upside'])
