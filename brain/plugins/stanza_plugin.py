#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  stanza_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_stanza(source, type, parameters):
	if parameters:
		node=xmpp.simplexml.XML2Node(unicode(parameters).encode('utf8'))
#		JCON.SendAndCallForResponse(node, handler_stanza_answ,{'type': type, 'source': source})
		JCON.send(node)
		return
	rep = u'you want to send ?'
	reply(source, type, rep)
	
#def handler_stanza_answ(coze, res, type, source):
#	if res:
#		reply(source, type, res.getData())
#		return
#	reply(source, type, u'глюк')

register_command_handler(handler_stanza, '!stanza', ['superadmin','muc','all'], 100, 'топка', '!stanza <payload>', ['!stanza aaabbb'])

