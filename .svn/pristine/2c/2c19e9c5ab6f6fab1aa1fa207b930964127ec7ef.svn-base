#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  ping_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

ping_pending=[]

def handler_ping(type, source, parameters):
	nick=parameters
	groupchat=source[1]
	iq = xmpp.Iq('get')
	id = 'p'+str(random.randrange(1, 1000))
	globals()['ping_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				if GROUPCHATS[groupchat][nick]['ishere']==0:
					reply(type, source, u'And, is he here? :-O')
					return
				param=nick
				jid=groupchat+'/'+nick
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+source[2]
		iq.setTo(jid)
		param=''
	t0 = time.time()
	JCON.SendAndCallForResponse(iq, handler_ping_answ,{'t0': t0, 'mtype': type, 'source': source, 'param': param})
	return

def handler_ping_answ(coze, res, t0, mtype, source, param):
	id = res.getID()
	if id in globals()['ping_pending']:
		globals()['ping_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
			t = time.time()
			rep = u'Pong from '
			if param:
				rep += param
			else:
				rep += u'you'
			rep+=u' '+str(round(t-t0, 3))+u' sec.'
		else:
			rep = u'failed!'
	reply(mtype, source, rep)
	
register_command_handler(handler_ping, COMM_PREFIX+'ping', ['info','muc','all', '*'], 0, 'Pings you, or some nickname or a server.', COMM_PREFIX+'ping [nick]', [COMM_PREFIX+'ping guy',COMM_PREFIX+'ping jsmart.web.id'])