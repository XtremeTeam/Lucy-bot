#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  features_plugin.py

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

def greetz_work(jid='',greet='',gch=''):
	DBPATH='settings/'+gch+'/greetz.txt'
	if check_file(gch,'greetz.txt'):
		greetzdb = eval(read_file(DBPATH))
		if jid and greet:
			if not jid in greetzdb.keys():
				greetzdb[jid]=jid
				greetzdb[jid]=greet
				write_file(DBPATH, str(greetzdb))
				return 1
			else:
				greetzdb[jid]=greet
				write_file(DBPATH, str(greetzdb))
				return 1
		elif jid:
			if jid in greetzdb.keys():
				del greetzdb[jid]
				write_file(DBPATH, str(greetzdb))
				return 1
			return 0
		else:
			return 0
		
def handler_greet(type,source,parameters):
	if not parameters:
		reply(type, source, u'And?')
		return
	parameters=parameters.strip()
	rawgreet = string.split(parameters, '=', 1)
	if not len(rawgreet)==2:
		reply(type, source, u'What was it?')
		return
	greet=rawgreet[1].strip()
	nicks=GROUPCHATS[source[1]].keys()
	if rawgreet[0].count('@')>0 and rawgreet[0].count('.')>0:
		jid=rawgreet[0]
	elif rawgreet[0] in nicks:
		jid=get_true_jid(source[1]+'/'+rawgreet[0])
	else:
		reply(type, source, u'I do not see that user here :-O')
		return
	if not greet:
		answ=greetz_work(jid,gch=source[1])
		if answ:
			reply(type, source, u'Deleted!')
			get_greetz(gch=source[1])
			return
		else:
			reply(type, source, u'Who?')
			return
	answ=greetz_work(jid,greet,source[1])
	if answ:
		reply(type, source, u'Aha!')
		get_greetz(gch=source[1])
	else:
		reply(type, source, u'What was it?')
		
def atjoin_greetz(groupchat, nick, aff, role):
	if time.time()-INFO['start']>10:	
	 jid=get_true_jid(groupchat+'/'+nick)
	 if groupchat in GREETZ.keys():
	 	if jid in GREETZ[groupchat]:
	 		msg(groupchat, nick+'> '+GREETZ[groupchat][jid])
	 		
def get_greetz(gch):
	grtfile='settings/'+gch+'/greetz.txt'
	try:
		grt = eval(read_file(grtfile))
		GREETZ[gch]=grt
	except:
		pass
			
register_command_handler(handler_greet, COMM_PREFIX+'greet', ['muc','all','*'], 20, 'Adds greeting for certain a nick or jid.', COMM_PREFIX+'greet <nick/jid>', [COMM_PREFIX+'greet guy=something',COMM_PREFIX+'greet guy@jsmart.web.id=anything'])	

register_join_handler(atjoin_greetz)
register_stage1_init(get_greetz)