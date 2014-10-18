#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  idle_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

idle_pending=[]
def handler_idle(type, source, parameters):
	idle_iq = xmpp.Iq('get')
	id='idle'+str(random.randrange(1000, 9999))
	globals()['idle_pending'].append(id)
	idle_iq.setID(id)
	idle_iq.addChild('query', {}, [], 'jabber:iq:last');
	if parameters:
		param = parameters.strip()
		idle_iq.setTo(param)
	else:
		param=CONNECT_SERVER
		idle_iq.setTo(param)
	JCON.SendAndCallForResponse(idle_iq, handler_idle_answ, {'type': type, 'source': source, 'param': param})
	
		
def handler_idle_answ(coze, res, type, source, param):
	id=res.getID()
	if id in globals()['idle_pending']:
		globals()['idle_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
			reply(type,source,u'That jabber server not found, or it falls down, or it forbids to look this information!')
			return
		elif res.getType() == 'result':
			sec = ''
			props = res.getPayload()
			if not props:
				reply(type,source,u'That jabber server had been power-off or it is not present!')
				return 
			for p in props:
				sec=p.getAttrs()['seconds']
				if not sec == '0':
					rep = param+u' already works for '+timeElapsed(int(sec))+'.'
	else:
		rep = u'Bug!'
	reply(type, source, rep)

def handler_userinfo_idle(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		if not parameters:
			reply(type,source,u'And?')
			return
		nick = parameters.strip()
		if nick==source[2]:
			reply(type,source,u'What should I say? ;)')
			return
		if GROUPCHATS[source[1]].has_key(nick) and GROUPCHATS[source[1]][nick]['ishere']==1:
			groupchat = source[1]
			idletime = int(time.time() - GROUPCHATS[groupchat][nick]['idle'])
			reply(type, source, nick+u' sleep '+timeElapsed(idletime)+u' ago.')
		else:
			reply(type,source,u'Are you sure that user is here? :-O')
			
register_command_handler(handler_idle, 'uptime', ['info','muc','all','*'], 10, 'Show uptime of certain server.', 'uptime <server>', ['uptime jsmart.web.id'])
register_command_handler(handler_userinfo_idle, 'idle', ['info','muc','all','*'], 10, 'Shows how long a user is nonactive.', 'idle <nick>', ['idle guy'])