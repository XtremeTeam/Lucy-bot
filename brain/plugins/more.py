#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  more_plugin.py

#  Initial Copyright © 2009 Als <als-als@ya.ru>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_more(type, source, parameters):
	if type!='private':
		if source[1] in GCHCFGS.keys() and GCHCFGS[source[1]]['more']==1:
			if LAST['gch'][source[1]]['msg']:
				reply(type,source, LAST['gch'][source[1]]['msg'])
	else:
		reply(type,source, u' A sense?')
			
def handler_more_outmsg(target, body, obody):
	if target in GCHCFGS.keys() and GCHCFGS[target]['more']==1:
		if hash(obody)!=LAST['gch'][target]['msg']:
			if len(obody)>MSG_CHATROOM_LIMIT:
				LAST['gch'][target]['msg']=obody[MSG_CHATROOM_LIMIT:]

def init_more(gch):
	if not 'more' in GCHCFGS[gch]:
		GCHCFGS[gch]['more']=1
	if GCHCFGS[gch]['more']:
		LAST['gch'][gch]['msg']=''
			
register_command_handler(handler_more, 'more', ['muc','all','*'], 0, 'Displays the rest of the messages that exceeded the limit of %d characters.' % (MSG_CHATROOM_LIMIT), 'more', ['more'])

register_outgoing_message_handler(handler_more_outmsg)
register_stage1_init(init_more)