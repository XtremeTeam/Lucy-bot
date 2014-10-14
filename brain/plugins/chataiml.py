#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin plugin
#  chataiml.py

#  edited by planb(planb@talkonaut.com)

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import aiml
import string
from string import *

def chat_pyaiml(type, source, body):
    replyy = k.respond(body, get_true_jid(source))
    reply(type, source, replyy)

def handler_pyaiml(type, source, body):
    if type == 'private': 
		if not COMMANDS.has_key(string.split(body)[0]):
			chat_pyaiml(type, source, body)
    if type == 'public'and get_bot_nick(source[1])!=source[2] and source[2]!='' and re.search('^'+get_bot_nick(source[1])+':',body)!=None:
                if not COMMANDS.has_key(string.split(body)[1]):
			chat_pyaiml(type, source, body.replace(get_bot_nick(source[1])+':','').strip())
			
#def stop_aiml
#    if 			
                            
		                    
    

register_message_handler(handler_pyaiml)
if __name__ == "__main__":
	load_aiml()
	pass
