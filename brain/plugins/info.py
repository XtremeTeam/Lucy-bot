#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  info_plugin.py

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'You are assured, that <'+nick+u'> is here?')
			return
		else:
			jidsource=groupchat+'/'+nick
			if get_true_jid(jidsource) == 'None':
				reply(type, source, u'i dont know')
				return
			truejid=get_true_jid(jidsource)
			if type == 'public':
				reply(type, source, u'private')
		reply('private', source, u'real jid of <'+nick+u'> --> '+truejid)
		
		
def handler_total_in_muc(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		inmuc=[]
		for x in GROUPCHATS[groupchat].keys():
			if GROUPCHATS[groupchat][x]['ishere']==1:
				inmuc.append(x)
		reply(type, source, u'I see here '+str(len(inmuc))+u' Users\n'+u', '.join(inmuc))
	else:
		reply(type, source, u'no users...')
		
		
def handler_bot_uptime(type, source, parameters):
	if INFO['start']:
		uptime=int(time.time() - INFO['start'])
		rep = u'I work without falling already '+timeElapsed(uptime)
		rep += u'\ni received %s messages, processed %s presences %s iq-queries, and also has executed %s Commands\n'%(str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
		if os.name=='posix':
			try:
				pr = os.popen('ps -o rss -p %s' % os.getpid())
				pr.readline()
				mem = pr.readline().strip()
			finally:
				pr.close()
			if mem: rep += u'Also by me it is eaten %s kb memmory, ' % mem
		(user, system,qqq,www,eee,) = os.times()
		rep += u'spent %.2f seconds, the processor is %.2f seconds System time and as a result %.2f of system-wide time\n' % (user, system, user + system)
		rep += u'I have generated all %s Streams, currently active %s flows' % (INFO['thr'], threading.activeCount())
	else:
		rep = u'аблом...'
	reply(type, source, rep)

register_command_handler(handler_getrealjid, 'truejid', ['info','admin','muc','all'], 20, 'shows the real jid of a nick. works only if bot is in same conference', 'truejid <nick>', ['truejid guy'])
register_command_handler(handler_total_in_muc, 'here', ['info','muc','all'], 10, 'Shows quantity of users currently in conference.', 'here', ['here'])
register_command_handler(handler_bot_uptime, 'botup', ['info','admin','all'], 10, 'Shows what is the time of the bot working without falling.', 'botup', ['botup'])
