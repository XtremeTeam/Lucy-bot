#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  eliza_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import eliza
therapist = eliza.eliza()

def handler_eliza_en(type,source, body):
	
	if type == 'public' and get_bot_nick(source[1])!=source[2] and source[2]!='' and re.search('^'+get_bot_nick(source[1])+':',body)!=None:
		result=therapist.respond(body.replace(get_bot_nick(source[1])+':','').strip())
		smsg(type,source, result)
	pass
	
#register_message_handler(handler_eliza_en)
