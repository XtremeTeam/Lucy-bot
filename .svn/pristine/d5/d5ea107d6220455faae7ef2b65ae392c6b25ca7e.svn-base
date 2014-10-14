#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  version_plugin.py

#  Initial Copyright Â© 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright Â© 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

version_pending=[]
def handler_version(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	iq = xmpp.Iq('get')
	id='vers'+str(random.randrange(1000, 9999))
	globals()['version_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		jid=groupchat+'/'+parameters.strip()
		if GROUPCHATS.has_key(groupchat):
			nicks = GROUPCHATS[groupchat].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				if GROUPCHATS[groupchat][nick]['ishere']==0:
					reply(type, source, u'he is here? :-O')
					return
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	JCON.SendAndCallForResponse(iq, handler_version_answ, {'type': type, 'source': source})
	return

def handler_version_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['version_pending']:
		globals()['version_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = '[no name]'
			version = '[no ver]'
			os = '[no os]'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			if name:
				rep =' \nclient: '+name
			if version:
				rep +=' \nversion: '+version
			if os:
				rep +=u' \nos: '+os
		else:
			rep = u'i dont see that person'
	else:
		rep = u'no such'
	reply(type, source, rep)
	
def handler_botver(type, source, parameters):
        reply(type, source, u'my version is:\nclient: Python2.7 \nVersion: Lucy (x-team bot)\nos: PocketPc windows mobile©')

register_command_handler(handler_botver, 'bv', ['info','muc','all'], 0, 'displays the bots version', 'bv', ['bv'])
register_command_handler(handler_version, ',', ['info','muc','all'], 0, 'The user or a server shows the information on the client.', ', <nick\server>', [',',', Nick',', jabber.aq'])
