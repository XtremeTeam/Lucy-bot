#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  invite_plugin.py

#  Initial Copyright © 2008 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def get_jid(gch, nick):
	nick = nick.replace('"','&quot;')
	sql = 'SELECT jid FROM users WHERE nick="%s";' % (nick)
	qres = querymuc('settings/'+gch+'/users.db',sql)
	
	if qres:
		jid = qres[0][0]
		return jid
	else:
		return ''

def check_jid(jid):
	parse_jid = jid.split('@')
	
	if len(parse_jid) == 2:
		if parse_jid[0] and parse_jid[1]:
			if parse_jid[1].count('.') >= 1 and parse_jid[1].count('.') <= 3:
				return True
			else:
				return False	
		else:
			return False
	else:
		return False

def split_reason(parameters):
	nijirel = parameters.split(':', 1)
	splited = ['','']	
		
	if len(nijirel) == 1:
		splited[0] = nijirel[0].strip()
		splited[1] = ''
	elif len(nijirel) == 2:
		splited[0] = nijirel[0].strip()
		splited[1] = nijirel[1].strip()
	return splited

def handler_invite_start(type, source, parameters):
	jid,nick_jid,reason='','',''
	groupchat = source[1]
	nick = source[2]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	sparams = split_reason(parameters)
	
	nick_jid = sparams[0]
	reason = sparams[1]
	
	if parameters:
		if not check_jid(nick_jid):
			jid = get_jid(groupchat,nick_jid)
			
			if not jid:
				reply(type,source,u'Are you sure, that \"'+nick_jid+u'\" was there?')
				return
		else:
			jid = nick_jid
			
		msg = xmpp.Message(to=groupchat)
		ID = 'inv'+str(random.randrange(1, 1000))
		
		msg.setID(ID)
		x=xmpp.Node('x')
		x.setNamespace('http://jabber.org/protocol/muc#user')
		inv=x.addChild('invite', {'to':jid})
		
		if reason:
			inv.setTagData('reason', reason +' (%s)' % (nick))
		else:
			inv.setTagData('reason', u'You are invited by '+nick+'.')
			
		msg.addChild(node=x)
		resp = JCON.send(msg)
		
		if resp == ID:
			reply(type,source,u'Done!')
	else:
		reply(type,source,u'And, who?')

register_command_handler(handler_invite_start, 'invite', ['muc','all','*'], 11, 'Invite specified user in the conference.', 'invite <nick|JID> [: reason]', ['invite guy', 'invite guy | come to us, we have fun ;)','invite guy@jsmart.web.id','invite guy@jsmart.web.id | We have a bussines!'])	