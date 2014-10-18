#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  dict_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import DICT
import urllib

def handler_dict_define(type, source, parameters):
	dc = DICT.DictConnection('dict.org')
	try:
		results = dc.get_definition(parameters.strip())
		if len(results):
			#reply = string.join(results[0], '\n')
			reply = 'http://www.dict.org/bin/Dict?Form=Dict1&Query=' + urllib.quote(parameters) + '&Strategy=*&Database=*'
			for result in results[:3]:
				reply += '\n\n' + string.join(result[:8], '\n')[:500][4:]
				if len(result) > 8:
					reply += ' . . .'
			reply = reply.replace('\n\n\n', '\n\n')
		else:
			reply = 'No Results'
	except:
		raise
		reply = 'Error'
	smsg(type, source, reply)

register_command_handler(handler_dict_define, 'define', ['fun','superadmin','muc','all'], 0, 'Defines a word using the DICT protocol.', 'define <word>', ['define neutron'])
