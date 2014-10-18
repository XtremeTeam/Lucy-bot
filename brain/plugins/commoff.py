#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  commoff_plugin.py

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

handler_pyaiml = 'Aiml'

def handler_commoff(type,source,parameters):
        if not source[1] in GROUPCHATS:
                reply(type, source, u'this command is available only in the conference')
                return
	na=['access','eval','login','logout','stanza','gaccess_set','leave','restart','gaccess_set','commands','sh','exec','commoff','common','Aiml']
	
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='settings/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if not y in commoff:
						commoff.append(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'						
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'The following commands has been disabled at this conference:\n'+valcomm
		if alrcomm:
			rep+=u'\nThe followings commands were not disabled, coz they are disabled already:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nThe following commands are unrecognize commands :\n'+notvalcomm
		if npcomm:
			rep+=u'\nIt is impossible to disable the followings commands in general:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		for x in commoff:
			vcnt+=1
			valcomm+=str(vcnt)+u') '+x+u'\n'
		if valcomm:
			rep=u'Disabled commands at this conference:\n'+valcomm
		else:
			rep=u'all of commands are enabled at this conference!'
		
	reply(type,source,rep.strip())
		
def handler_common(type,source,parameters):
	if not source[1] in GROUPCHATS:
			reply(type, source, u'this command is available only in the conference')
			return
	na=['access','eval','login','logout','stanza','gaccess_set','leave','restart','gaccess_set','commands','sh','exec','commoff','common','Aiml']

	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,rep,commoff=u'',u'',u'',u'',0,0,0,0,u'',[]
	if not source[1] in COMMOFF:
		get_commoff(source[1])
	commoff=COMMOFF[source[1]]
	DBPATH='settings/'+source[1]+'/config.cfg'
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if y in commoff:
						commoff.remove(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'The following commands has been enabled at this conference:\n'+valcomm
		if alrcomm:
			rep+=u'\nThe followings commands were not enabled, coz they are enabled already:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nThe following commands are unrecognize commands :-) :\n'+notvalcomm
		if npcomm:
			rep+=u'\nThe following commands are not disabled at all:\n'+npcomm
		if not GCHCFGS[source[1]].has_key('commoff'):
			GCHCFGS[source[1]]['commoff']='commoff'
			GCHCFGS[source[1]]['commoff']=[]
		GCHCFGS[source[1]]['commoff']=commoff
		write_file(DBPATH, str(GCHCFGS[source[1]]))
		get_commoff(source[1])
	else:
		rep=u'And?'
		
	reply(type,source,rep.strip())
	
def get_commoff(gch):
	try:
		if GCHCFGS[gch].has_key('commoff'):
			commoff=GCHCFGS[gch]['commoff']
			COMMOFF[gch]=commoff
		else:
			COMMOFF[gch]=gch
			COMMOFF[gch]=[]
	except:
		pass
	
register_command_handler(handler_commoff, 'commoff', ['admin','muc','all','*'], 20, 'Disable certain commands for the current conf, without parameters shows a list of commands that already disabled.', 'commoff [commands]', ['commoff','commoff %spoke %sdisco %sversion'])
register_command_handler(handler_common, 'common', ['admin','muc','all','*'], 20, 'Enable certain commands for current conf.', 'common [commands]', ['common %spoke %sdisco %sversion'])

register_stage1_init(get_commoff)
