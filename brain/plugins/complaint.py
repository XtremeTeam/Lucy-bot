#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  complaint_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_complaint(type, source, parameters):
	if type == 'public':
		reply(type, source, u'this command works only in my private!')
	elif type == 'private':
		groupchat=source[1]
		if GROUPCHATS.has_key(groupchat):
			nicks = GROUPCHATS[groupchat].keys()
			args = parameters.split(' ')
			nick = args[0].strip()
			body = ' '.join(args[1:])
			if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['ishere']==1:		
				jidsource=groupchat+'/'+nick
				if user_level(jidsource,groupchat)>=15:
					reply(type,source,u'steps will be taken ]:->')
					return			
				if len(nick)>20 or len(body)>100:
					reply(type, source, u'u have written too much?')
					return
				for x in nicks:
					jid=groupchat+'/'+x
					if user_level(jid,groupchat)>=15 and GROUPCHATS[groupchat][x]['status'] in ['online','away','chat']:
						msg(jid, u'user <'+source[2]+u'>\ncomplaint on <'+nick+u'>\nreason <'+body+u'>\n\nyou can ban (ban '+nick+u' `reason`) or kick (kick '+nick+u' `reason`) this nick from my private now')
				reply(type, source, u'complaint to <'+nick+u'> has been sent vto all moderators of the room. If the complaint will be consider true, then you will be banned!')
			else:
				reply(type,source,u'are you sure, that <'+nick+u'>is her? Huh!!?')
				
register_command_handler(handler_complaint, COMM_PREFIX+'complaint',  ['muc','all'], 10, 'To complain on certain nick for the certain reason. Works only for me in private!', 'complaint <nick> <reason>', ['complaint Nick7 flooding'])
