#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin plugin
#  access_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.



def admin_getglobadmins(type, source, parameters):
        res1 = u'List of global managers:'
        res2 = u'Ignore List:'
        res3 = u'List of local administrators:'
        res4 = u'List of local ignore:'
        
        res1_ = u''
        res2_ = u''
        res3_ = u''
        res4_ = u''
        i = 0
        j = 0
        k = 0
        a = 0
        if len(GLOBACCESS) == 1:
                reply(type, source, u'No global access')
                return
        for jid in GLOBACCESS:
                if GLOBACCESS[jid] >=41:
                        i += 1
                        if GLOBACCESS[jid] == 100:
                                inf = ''
                        else:
                                inf = ': '+str(GLOBACCESS[jid])
                        res1_+= '\n'+str(i)+'. '+jid+inf
                        
                if GLOBACCESS[jid] <0:
                        j += 1
                        if GLOBACCESS[jid] == -100:
                                inf_ = ''
                        else:
                                inf_ = ': '+str(GLOBACCESS[jid])
                        res2_ += '\n'+str(j)+'. '+jid+inf_
#*************************************************************************#

        for conf in ACCBYCONF:
                for jid in ACCBYCONF[conf]:
                        if ACCBYCONF[conf][jid] >= 41:
                                k +=1
                                if ACCBYCONF[conf][jid] == 100:
                                        inf__ = ''
                                else:
                                        inf__ = ': '+str(ACCBYCONF[conf][jid])
                                res3_ += '\n'+str(k)+'. '+jid+inf__
                        if ACCBYCONF[conf][jid] <= 0:
                                a +=1
                                if ACCBYCONF[conf][jid] == -100:
                                        inf___ = ''
                                else:
                                        inf___ = ': '+str(ACCBYCONF[conf][jid])
                                res4_ += '\n'+str(a)+'. '+jid+inf___                                
        if res1_ == '':
                res1_ = u'\empty'
        if res2_ == '':
                res2_ = u'\empty'
        if res3_ == '':
                res3_ = u'\empty'
        if res4_ == '':
                res4_ = u'\empty'
                
        res1 += res1_
        res2 += res2_
        res3 += res3_
        res4 += res4_
        
        reply(type, source, res1+'\n'+res2+'\n'+res3+'\n'+res4)

def view_access(type, source, parameters):
	accdesc
	if not parameters:
		level=str(user_level(source[1]+'/'+source[2], source[1]))
		if level in accdesc.keys():
			levdesc=accdesc[level]
		else:
			levdesc=''		
		reply(type, source, level+u' '+levdesc)
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'This is possible only in the conference!')
			return
		nicks = GROUPCHATS[source[1]].keys()
		if parameters.strip() in nicks:
			level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
			if level in accdesc.keys():
				levdesc=accdesc[level]
			else:
				levdesc=''
			reply(type, source, level+' '+levdesc)
		else:
			reply(type, source, u'the user is not here!')

def set_access_local(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'only use this in the conference room')
		return
	splitdata = string.split(parameters)
	if len(splitdata) > 1:
		try:
			int(splitdata[1].strip())
		except:
			reply(type, source, u'Bad expression. Read help on using this command!')
			return				
		if int(splitdata[1].strip())>100 or int(splitdata[1].strip())<-100:
			reply(type, source, u'Bad expression. Read help on using this command')
			return		
	nicks=GROUPCHATS[source[1]]
	if not splitdata[0].strip() in nicks and GROUPCHATS[source[1]][splitdata[0].strip()]['ishere']==0:
		reply(type, source, u'Either the user is not here or you mispelled the nickname')
		return
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	tjidsource=get_true_jid(source)
	groupchat=source[1]
	jidacc=user_level(source, groupchat)
	toacc=user_level(tjidto, groupchat)

	if len(splitdata) > 1:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				if int(splitdata[1]) > int(jidacc):
					reply(type, source, u'Either the user is not here or you mispelled the nickname')
					return
			elif int(toacc) > int(jidacc):
				reply(type, source, u'You do not have Admin Privileges')
				return		
			elif int(splitdata[1]) >= int(jidacc):
				reply(type, source, u'Either the user is not here or you mispelled the nickname')
				return	
	else:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				pass
			elif int(toacc) > int(jidacc):
				reply(type, source, u'You do not have Admin Privileges')
				return

	if len(splitdata) == 1:		
		change_access_perm(source[1], tjidto)
		if splitdata[0].strip()==source[2]:
			reply(type, source, u'Permanent access removed. This will take effect when I reboot')
		else:
			reply(type, source, u'Permanent access %s removed. This will take effect when I reboot' % splitdata[0].strip())
	elif len(splitdata) == 2:
		change_access_temp(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'temporally access granted!')
	elif len(splitdata) == 3:
		change_access_perm(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'permanent access granted!')		
		
def set_access_global(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'You can only use this in a conference!')
		return
	if parameters:
		splitdata = parameters.strip().split()
		if len(splitdata)<1 or len(splitdata)>2:
			reply(type, source, u'hmm could you Repeat that? i was busy listening to music!')
			return
		nicks=GROUPCHATS[source[1]].keys()
		if not splitdata[0].strip() in nicks and GROUPCHATS[source[1]][splitdata[0].strip()]['ishere']==0:
			reply(type, source, u'that user is not here!')
			return
		tjidto=get_true_jid(source[1]+'/'+splitdata[0])
		if len(splitdata)==2:
			change_access_perm_glob(tjidto, int(splitdata[1]))
			reply(type, source, u'premissions granted')
		else:
			change_access_perm_glob(tjidto)
			reply(type, source, u'Permissions Revoked')
			
def get_access_levels():
	global GLOBACCESS
	global ACCBYCONFFILE
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	ACCBYCONFFILE = eval(read_file(ACCBYCONF_FILE))


register_command_handler(admin_getglobadmins, COMM_PREFIX+'accesses', ['superadmin','new','all'], 100, 'Shows all global and local access', 'accesses', ['accesses'])	
register_command_handler(view_access, COMM_PREFIX+'access', ['access','admin','all','*'], 0, 'Shows the access level specified nickname.\n-100 - complete ignore all messages from from such user at kernel level\n-1 - can not do anything\n0 - a very limited number of commands and macros, automatically assigned as visitor\n10 - standard set of commands and macros, automatically assigned participant\n11 - extended set of commands and macros (such as access to !!!), automatically assigned as member\n15 (16) - moderator set of commands and macros, automatically assigned as moderator\n20 - admin set of commands and macros, automatically assigned as admin\n30 - owner set of commands and macros, automatically assigned as owner\n40 - not implemented for all commands, allows the user access to some commands and leave th bot from the conferences\n100 - bot admin, all commands are allowed', COMM_PREFIX+'access [nick]', [COMM_PREFIX+'access', COMM_PREFIX+'access guy'])
register_command_handler(set_access_local, COMM_PREFIX+'givetemp', ['access','admin','all','*'], 100, 'Set or remove local access for a particular nickname.\nWrite without level after the nick to remove the access, required the bot rejoin conference. If the third parameter "forever" specified, the change take place forever, otherwise the access dissapear when the bot rejoin the conference.\n-100 - complete ignore all messages from from such user at kernel level\n-1 - can not do anything\n0 - a very limited number of commands and macros, automatically assigned as visitor\n10 - standard set of commands and macros, automatically assigned participant\n11 - extended set of commands and macros (such as access to !!!), automatically assigned as member\n15 (16) - moderator set of commands and macros, automatically assigned as moderator\n20 - admin set of commands and macros, automatically assigned as admin\n30 - owner set of commands and macros, automatically assigned as owner\n40 - not implemented for all commands, allows the user access to some commands and leave th bot from the conferences\n100 - bot admin, all commands are allowed', COMM_PREFIX+'givetemp <nick> <level> [forever]', [COMM_PREFIX+'access_set guy 100', COMM_PREFIX+'access_set guy 100 something'])
register_command_handler(set_access_global, COMM_PREFIX+'giveglob', ['access','superadmin','all','*'], 100, 'Set or remove global access for a particular nickname.\nWrite without level after the nick to remove the access.', COMM_PREFIX+'giveglob <nick> <level>', [COMM_PREFIX+'giveglob Nickname 100',COMM_PREFIX+'giveglob (nickname)'])

register_stage0_init(get_access_levels)
