#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  status_plugin.py

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

def handler_status(type, source, parameters):
	if parameters:
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
			stmsg=GROUPCHATS[source[1]][parameters]['stmsg']
			status=GROUPCHATS[source[1]][parameters]['status']
			if stmsg:
				reply(type,source, parameters+u' now '+status+u' ('+stmsg+u')')
			else:
				reply(type,source, parameters+u' now '+status)
		else:
			reply(type,source, u'Аnd then? :-O')
	else:
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
			stmsg=GROUPCHATS[source[1]][source[2]]['stmsg']
			status=GROUPCHATS[source[1]][source[2]]['status']
			if stmsg:
				reply(type,source, u'You now '+status+u' ('+stmsg+u')')
			else:
				reply(type,source, u'You now '+status+'.')

def status_change(prs):
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	if not stmsg:
		stmsg=''
	status = prs.getShow()
	if not status:
		status=u'online'
	if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat]:
		GROUPCHATS[groupchat][nick]['status']=status
		GROUPCHATS[groupchat][nick]['stmsg']=stmsg

register_presence_handler(status_change)

register_command_handler(handler_status,  'status', ['info','muc','all','*'], 0, 'Shows the status and status message (if any) specified nick.',  'status <user>', [ 'status',  'status guy'])