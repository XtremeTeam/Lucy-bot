#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  macro_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# [[u'пинг', u'Gigabyte', SOURCE, 1800],[[u'тест', u'', SOURCE, 60]],[[u'апр', u'Gigabyte', SOURCE, 800]]]

timer_count = 4

import time


def admin_getlistconf(type, source, parameters):
	DBPATH='settings/'+source[1]+'/conflist.cfg'
	if check_file(source[1],'conflist.cfg'):
		setup = eval(read_file(DBPATH))
	try:
		set_nomer = setup['nomer']
	except:
		setup['nomer'] = '1'
		set_nomer = setup['nomer']
#*******************************************
	try:
		set_conf = setup['conf']
	except:
		setup['conf'] = '1'
		set_conf = setup['conf']
#*******************************************
	try:
		set_botnick = setup['botnick']
	except:
		setup['botnick'] = '1'
		set_botnick = setup['botnick']
#*******************************************
	try:
		set_allusers = setup['allusers']
	except:
		setup['allusers'] = '1'
		set_allusers = setup['allusers']
#*******************************************
	try:
		set_redusers = setup['redusers']
	except:
		setup['redusers'] = '1'
		set_redusers = setup['redusers']
#*******************************************
	try:
		set_yellusers = setup['yellusers']
	except:
		setup['yellusers'] = '1'
		set_yellusers = setup['yellusers']
#*******************************************
	try:
		set_botstatus = setup['botstatus']
	except:
		setup['botstatus'] = '1'
		set_botstatus = setup['botstatus']
#*******************************************
	try:
		set_botadmin = setup['botadmin']
	except:
		setup['botadmin'] = '1'
		set_botadmin = setup['botadmin']
	write_file(DBPATH, str(setup))
#*******************************************
	try:
		set_serverdef = setup['serverdef']
	except:
		setup['serverdef'] = 'xtreme.im'
		set_serverdef = setup['serverdef']
	write_file(DBPATH, str(setup))
#*******************************************
	try:
		set_shortserver = setup['shortserver']
	except:
		setup['shortserver'] = '1'
		set_shortserver = setup['shortserver']
	write_file(DBPATH, str(setup))


	if parameters != '':
		command = parameters.split()
		if (len(command) == 1) & (command[0] == u'find'):
			reply(type, source, u'what should i find?')
			return
		if (len(command) == 1) & (command[0] == u'option'):
			reply(type, source, u'Customize the list of display information in a conferences, command option:\n * number\n * conf\n * botnick\n * allusers\n * redusers\n * yellusers\n * botstatus\n * botadmin\n ** shortserver\n ** servdef\n *** find - search for combinations of letters in the conference')
			return
		allkeys = [u'number', u'conf', u'botnick', u'allusers', u'redusers', u'yellusers', u'botstatus', u'botadmin', u'shortserver', u'servdef'] 
		if (len(command) == 2) & (command[0] == u'option'):
			if not command[1] in allkeys:
				reply(type, source, u'invalid option')
				return
			if command[1] == u'number':
				if setup['nomer'] == '1':
					res = u'enabled'
				if setup['nomer'] == '0':
					res = u'disabled'
			if command[1] == u'conf':
				if setup['conf'] == '1':
					res = u'enabled'
				if setup['conf'] == '0':
					res = u'disabled'
			if command[1] == u'botnick':
				if setup['botnick'] == '1':
					res = u'enabled'
				if setup['botnick'] == '0':
					res = u'disabled'
			if command[1] == u'allusers':
				if setup['allusers'] == '1':
					res = u'enabled'
				if setup['allusers'] == '0':
					res = u'disabled'
			if command[1] == u'redusers':
				if setup['redusers'] == '1':
					res = u'enabled'
				if setup['redusers'] == '0':
					res = u'disabled'
			if command[1] == u'yellusers':
				if setup['yellusers'] == '1':
					res = u'enabled'
				if setup['yellusers'] == '0':
					res = u'disabled'
			if command[1] == u'botstatus':
				if setup['botstatus'] == '1':
					res = u'enabled'
				if setup['botstatus'] == '0':
					res = u'disabled'
			if command[1] == u'botadmin':
				if setup['botadmin'] == '1':
					res = u'enabled'
				if setup['botadmin'] == '0':
					res = u'disabled'
			if command[1] == u'shortserver':
				if setup['shortserver'] == '1':
					res = u'enabled'
				if setup['shortserver'] == '0':
					res = u'disabled'
			if command[1] == u'serverdef':
				res = setup['serverdef']


			reply(type, source, u'option '+command[1]+u' are available: '+res)
			return
		if (len(command) == 3) & (command[0] == u'option'):
			if not command[1] in allkeys:
				reply(type, source, u'invalid option')
				return

			if command[1] == u'number':
				if (command[2] == '1') | (command[2] == '0'):
					set_nomer = command[2]
					setup['nomer'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display number '+res)
			if command[1] == u'conf':
				if (command[2] == '1') | (command[2] == '0'):
					set_conf = command[2]
					setup['conf'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display conf '+res)
			if command[1] == u'botnick':
				if (command[2] == '1') | (command[2] == '0'):
					set_botnick = command[2]
					setup['botnick'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display botnick '+res)
			if command[1] == u'allusers':
				if (command[2] == '1') | (command[2] == '0'):
					set_allusers = command[2]
					setup['allusers'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display allusers '+res)
			if command[1] == u'redusers':
				if (command[2] == '1') | (command[2] == '0'):
					set_redusers = command[2]
					setup['redusers'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display moderators '+res)
			if command[1] == u'yellusers':
				if (command[2] == '1') | (command[2] == '0'):
					set_yellusers = command[2]
					setup['yellusers'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display member/participants '+res)
			if command[1] == u'botstatus':
				if (command[2] == '1') | (command[2] == '0'):
					set_botstatus = command[2]
					setup['botstatus'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display role of bot '+res)
			if command[1] == u'botadmin':
				if (command[2] == '1') | (command[2] == '0'):
					set_botadmin = command[2]
					setup['botadmin'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'display botadmin '+res)
			if command[1] == u'shortserver':
				if (command[2] == '1') | (command[2] == '0'):
					set_shortserver = command[2]
					setup['shortserver'] = command[2]
					write_file(DBPATH, str(setup))
					if command[2] == '1':
						res = u'enabled'
					if command[2] == '0':
						res = u'disabled'
					reply(type, source, u'use short server '+res)
			if command[1] == u'serverdef':
				if (command[2].count('.') > 0):
					set_serverdef = command[2]
					setup['serverdef'] = command[2]
					write_file(DBPATH, str(setup))
					res = command[2]
					reply(type, source, u'set default server: '+res)
			return
#********************************************************
#	if (len(command) == 1) & (command[0] == u'найти'):
#********************************************************
	use = 0
	commhelp = ''
	if set_nomer == '1':
		commhelp += u'[#]'
	if set_conf == '1':
		commhelp += u'[conf]'
	if set_botnick == '1':
		commhelp += u'[botnick]'
	if set_allusers == '1':
		commhelp += u'(allusers)'
	if set_redusers == '1':
		commhelp += u'[redusers]'
	if set_yellusers == '1':
		commhelp += u'[yellusers]'
	if set_botstatus == '1':
		commhelp += u'[botrole]'
	if set_botadmin == '1':
		commhelp += u'[botadmin]'

	out = u'List of conf total: ('+str(len(GROUPCHATS.keys()))+u'):\n'+commhelp+'\n'
	len_room_mas = len( (GROUPCHATS.keys()) )
	if (parameters != ''):
		if (command[0] == u'find'):
			for i in range(0, len_room_mas):
				if (GROUPCHATS.keys()[i].count(command[1]) > 0):
					botnick = get_bot_nick(GROUPCHATS.keys()[i])
					moder = 0
					member = 0
					botadmin = 0
					allusers = 0
					use += 1
					for j in range(0, len(GROUPCHATS[GROUPCHATS.keys()[i]].keys())):
						if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ishere'] == 1:
	
							jid_nick = GROUPCHATS.keys()[i]+'/'+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]
							dsource = [jid_nick, 'GROUPCHATS.keys()[i]', 'GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]']
							if user_level(dsource, GROUPCHATS.keys()[i]) > 65:
								botadmin = botadmin + 1

							if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ismoder'] == 1:
								moder = moder + 1
							if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ismoder'] == 0:
								member = member + 1
							allusers = moder + member

							status = u'<admin>'
							if (moder == 0) & (member == 0):
								status = u'<error>'
							if (moder == 0) & (member > 0) & (len(GROUPCHATS.keys()) > 0):
								status = u'<no admin>'
							if (GROUPCHATS.keys()[i].count('@conference.'+set_serverdef) > 0) & (set_shortserver == '1'):
								ff = GROUPCHATS.keys()[i].split('@')
								conf = ff[0] + '@...'
							else:
								conf = GROUPCHATS.keys()[i]
							if botadmin > 0:
								bbotadmin = str(botadmin)
							else:
								bbotadmin = ''
					if set_nomer == '1':
						out +=str(i+1)+'. '
					if set_conf == '1':
						out +=conf + ' '
					if set_botnick == '1':
						out +='['+botnick+']'
					if set_allusers == '1':
						out +='(' + str(allusers) +')'
					if set_redusers == '1':
						out +=str(moder)
					if set_yellusers == '1':
						out +='/'+str(member)
					if set_botstatus == '1':
						out +=' ' + status + ' '
					if set_botadmin == '1':
						out +=bbotadmin
					out +='\n'

		#out +=str(i+1)+'. '+conf +' ['+botnick+'] (' + str(allusers) +') '+str(moder)+'/'+str(member)+' '+status+' '+bbotadmin+'\n'
			if use > 0:
				out = u'found '+str(use)+u' conf:\n' + out
#				msg(source[1], out)
				reply(type, source, out)
			if use == 0:
				out = u'nothing found :-('
#				msg(source[1], out)
				reply(type, source, out)
			return

	if (parameters == ''):
		for i in range(0, len_room_mas):
			if (GROUPCHATS.keys()[i].count('@')):
				botnick = get_bot_nick(GROUPCHATS.keys()[i])
				moder = 0
				member = 0
				botadmin = 0
				allusers = 0
				for j in range(0, len(GROUPCHATS[GROUPCHATS.keys()[i]].keys())):
					if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ishere'] == 1:
						use += 1
						jid_nick = GROUPCHATS.keys()[i]+'/'+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]
						dsource = [jid_nick, 'GROUPCHATS.keys()[i]', 'GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]']
						if user_level(dsource, GROUPCHATS.keys()[i]) > 65:
							botadmin = botadmin + 1

						if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ismoder'] == 1:
							moder = moder + 1
						if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ismoder'] == 0:
							member = member + 1
						allusers = moder + member

						status = u'<admin>'
						if (moder == 0) & (member == 0):
							status = u'<error>'
						if (moder == 0) & (member > 0) & (len(GROUPCHATS.keys()) > 0):
							status = u'<no admin>'
						if (GROUPCHATS.keys()[i].count('@conference.'+set_serverdef) > 0) & (set_shortserver == '1'):
							ff = GROUPCHATS.keys()[i].split('@')
							conf = ff[0] + '@...'
						else:
							conf = GROUPCHATS.keys()[i]
						if botadmin > 0:
							bbotadmin = str(botadmin)
						else:
							bbotadmin = ''
				if set_nomer == '1':
					out +=str(i+1)+'. '
				if set_conf == '1':
					out +=conf + ' '
				if set_botnick == '1':
					out +='['+botnick+']'
				if set_allusers == '1':
					out +='(' + str(allusers) +')'
				if set_redusers == '1':
					out +=str(moder)
				if set_yellusers == '1':
					out +='/'+str(member)
				if set_botstatus == '1':
					out +=' ' + status + ' '
				if set_botadmin == '1':
					out +=bbotadmin
				out +='\n'

		#out +=str(i+1)+'. '+conf +' ['+botnick+'] (' + str(allusers) +') '+str(moder)+'/'+str(member)+' '+status+' '+bbotadmin+'\n'

		if use > 0:
#			msg(source[1], out)
			reply(type, source, out)
		if use == 0:
#			out = u'nothing else :-('
			msg(source[1], out)
			reply(type, source, out)
		return


def admin_searchman(type, source, parameters):
	jid = parameters
	confs = ''
	t = 0
	
	for i in range(0, len(GROUPCHATS.keys())):
		for j in range(0, len(GROUPCHATS[GROUPCHATS.keys()[i]].keys())):
			#confs += GROUPCHATS.keys()[i]
			#print str(i) + ' ' + str(j) 
			truejid = get_true_jid(GROUPCHATS.keys()[i]+'/'+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j])
			#print truejid
			truejid = truejid.lower()
			nick = GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]
			jid = jid.lower()
			nick = nick.lower()
			if (truejid.count(jid)>0) | (nick.count(jid)>0):
				t += 1
				confs += str(t)+'. '+ GROUPCHATS.keys()[i] + ' ('+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]+') '+truejid+'\n'
	if confs == '':
		aa = u'upon request, I did not find it! =('
		reply(type,source,u'sent to private')
	else:
		aa = u'The user found at:\n[#][conf][(nick)][jid]\n'+ confs
		reply(type,source,u'sent to private')
	reply('private', source, aa)




def time_now():
	weekday = [u'Sun', u'Tue', u'Wed', u'Thu', u'Fri', u'Sat', u'Sun']
	mounthall = [u'Jan', u'Feb', u'Mar', u'Apr', u'May', u'Jun', u'Jul', u'Aug', u'Sep', u'Oct', u'Nov', u'Dec']
	week_ = time.strftime('%w', time.localtime()).decode('utf-8')
	week = weekday[int(week_)-1]
	month_ = time.strftime('%m', time.localtime()).decode('utf-8')
	month = mounthall[int(month_)-1]
	year = time.strftime('%y', time.localtime()).decode('utf-8')
	day = time.strftime('%d', time.localtime()).decode('utf-8')

	hour = time.strftime('%H', time.localtime()).decode('utf-8')
	min = time.strftime('%M', time.localtime()).decode('utf-8')
	sec = time.strftime('%S', time.localtime()).decode('utf-8')

	return [day, month_, year, hour, min, sec]

	#reply(type, source, u'Дата и время сервера (+6):\n '+week +' '+ day +' '+ month +' '+ year +' '+ hour +':'+min+'.'+sec)
	

#def admin_logingrecentusers_prs(prs):
#        fromjid = prs.getFrom()
#        nick = fromjid.getResource()
#        ptype = prs.getType()
#        jid = get_true_jid(fromjid)
#        groupchat = fromjid.getStripped()
#        
#        file='settings/'+groupchat+'/userslog.log'
#        if check_file(groupchat,'userslog.log'):
#		uslog = eval(read_file(file))
#	else:
#                print 'Error create or read userlog file'
#                return
#        
#        #print 'sss'
#        try:
#                uslog[jid][3] = time_now()
#                uslog[jid][6] = 'io'
#                if not nick in uslog[jid][2]:
#                        uslog[jid][2] += [nick]
#        except:
#                uslog[jid] = [0, 0, [nick], time_now(), '', '0', 'io']
#        write_file(file, str(uslog))
#                
#
#def admin_logingrecentusers_leave(groupchat, nick, reason, code):
#        #print reason
#
#        file='settings/'+groupchat+'/userslog.log'
#        if check_file(groupchat,'userslog.log'):
#		uslog = eval(read_file(file))
#	else:
#                print 'Error create or read userlog file'
#                return
#        jid = get_true_jid(groupchat+'/'+nick)
#        try:
#                # [Количество входов, Количество выходов, [Используемые ники], [дата последнего появления в формате [число][месяц][год][час][минута][секунда]]]
#                uslog[jid][1] += 1
#                uslog[jid][3] = time_now()
#                if reason:
#                        uslog[jid][4] = reason
#                else:
#                        uslog[jid][4] = ''
#                uslog[jid][5] = code
#                uslog[jid][6] = 'out'
#                if not nick in uslog[jid][2]:
#                        uslog[jid][2] += [nick]
#                        
#        except:
#                if reason:
#                        uslog[jid] = [0, 0, [nick], time_now(), reason, code, 'out']
#                else:
#                        uslog[jid] = [0, 0, [nick], time_now(), '', code, 'out']
#
#        write_file(file, str(uslog))
#
#def admin_logingrecentusers(groupchat, nick, aff, role):
#        file='settings/'+groupchat+'/userslog.log'
#        if check_file(groupchat,'userslog.log'):
#		uslog = eval(read_file(file))
#	else:
#                print 'Error create or read userlog file'
#                return
#        jid = get_true_jid(groupchat+'/'+nick)
#        try:
#                # [Количество входов, Количество выходов, [Используемые ники], [дата последнего появления в формате [число][месяц][год][час][минута][секунда]]]
#                uslog[jid][0] += 1
#                uslog[jid][3] = time_now()
#                uslog[jid][4] = ''
#                uslog[jid][5] = '0'
#                uslog[jid][6] = 'in'
#                if not nick in uslog[jid][2]:
#                        uslog[jid][2] += [nick]
#                        
#        except:
#                uslog[jid] = [0, 0, [nick], time_now(), '', '0', 'in']
#
#        write_file(file, str(uslog))
#        
#
#def admin_getrecentusers(type, source, parameters):
#        showall = 'off'
#        res = ''
#        mode = ''
#        rs = ''
#        date1 = [0,0,0]
#        date2 = [0,0,0]
#        time = time_now()
#        if parameters != '':
#                par = parameters.split()
#                if len(par) == 2:
#                        if par[0] == 'jid':
#                                if par[1] == 'on':
#                                        GCHCFGS[source[1]]['showjidrecus'] = 'on'
#                                        jd = GCHCFGS[source[1]]['showjidrecus']
#                                        DBPATH='settings/'+source[1]+'/config.cfg'
#                                        write_file(DBPATH, str(GCHCFGS[source[1]]))
#                                        reply(type, source, u'display JIDs enabled')
#                                        return
#                                if par[1] == 'off':
#                                        GCHCFGS[source[1]]['showjidrecus'] = 'off'
#                                        jd = GCHCFGS[source[1]]['showjidrecus']
#                                        DBPATH='settings/'+source[1]+'/config.cfg'
#                                        write_file(DBPATH, str(GCHCFGS[source[1]]))
#                                        reply(type, source, u'display JIDs disabled')
#                                        return
#                        if par[0] == u'show':
#                                if par[1] == u'all':
#                                        showall = 'on'
#                        if par[0] == u'find':
#                                mode = 'serarch'
#                                if par[1] != '':
#                                        spar = par[1]
#                
#        file='settings/'+source[1]+'/userslog.log'
#        if check_file(source[1],'userslog.log'):
#		uslog = eval(read_file(file))
#	else:
#                print 'Error create or read userlog file'
#                return
#        try:
#                jd = GCHCFGS[source[1]]['showjidrecus']
#        except:
#                GCHCFGS[source[1]]['showjidrecus'] = 'off'
#                jd = GCHCFGS[source[1]]['showjidrecus']
#                DBPATH='settings/'+source[1]+'/config.cfg'
#                write_file(DBPATH, str(GCHCFGS[source[1]]))
#
#
#        i = 0
#        jid = ''
#        for jid in uslog:
#                rs = ''
#                ce = uslog[jid][0]
#                ci = uslog[jid][1]
#                if uslog[jid][5] == '307':
#                                rs = u' | kick'
#                if uslog[jid][5] == '301':
#                                rs = u' | ban'
#                if uslog[jid][5] == '0':
#                        rs = u''
#                if uslog[jid][4] != '':
#                        rs += u' - ' + uslog[jid][4]
#                date = uslog[jid][3][0]+'.'+uslog[jid][3][1]+'.'+uslog[jid][3][2]+' | '+uslog[jid][3][3]+':'+uslog[jid][3][4]+':'+uslog[jid][3][5]
#                
#                nicks = '['
#                if len(uslog[jid][2]) == 1:
#                        nicks += uslog[jid][2][0]
#                else:
#                        for nick in uslog[jid][2]:
#                                nicks += nick+ ', '
#                                
#                if (date1[0] == 0) & (date1[1] == 0) & (date1[2] == 0):
#                        date1[0] = int(uslog[jid][3][0])
#                        date1[1] = int(uslog[jid][3][1])
#                        date1[2] = int(uslog[jid][3][2])
#                if (date2[0] == 0) & (date2[1] == 0) & (date2[2] == 0):
#                        date2[0] = int(uslog[jid][3][0])
#                        date2[1] = int(uslog[jid][3][1])
#                        date2[2] = int(uslog[jid][3][2])
#
#                if int(uslog[jid][3][2]) <= date1[2]:
#                        if int(uslog[jid][3][1]) <= date1[1]:
#                                if int(uslog[jid][3][0]) <= date1[0]:
#                                        date1[0] = int(uslog[jid][3][0])
#                                        date1[1] = int(uslog[jid][3][1])
#                                        date1[2] = int(uslog[jid][3][2])
#                if int(uslog[jid][3][2]) >= date2[2]:
#                        if int(uslog[jid][3][1]) >= date2[1]:
#                                if int(uslog[jid][3][0]) >= date2[0]:
#                                        date2[0] = int(uslog[jid][3][0])
#                                        date2[1] = int(uslog[jid][3][1])
#                                        date2[2] = int(uslog[jid][3][2])
#                dat = str(date1[0])+'.'+str(date1[1])+'.'+str(date1[2])+' - '+str(date2[0])+'.'+str(date2[1])+'.'+str(date2[2])
#                        
#                nicks += ']'
#                if jd == 'on':
#                        jid_ = jid
#                else:
#                        if jd == 'off':
#                                jid_ = u'<JID>'
#                        else:
#                                jid_ = u'<хз>'
#                if ((time[0] == uslog[jid][3][0]) & (time[1] == uslog[jid][3][1]) & (time[2] == uslog[jid][3][2])) & (showall == 'off') & (mode != 'serarch'):
#                        i += 1
#                        res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+')' + rs +'\n'
#                        
#                if (showall == 'on')  & (mode != 'serarch'):
#                        i += 1
#                        res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+') | '+date + rs +'\n'
#                if mode == 'serarch':
#                        if (jid.count(spar)>0):
#                                i += 1
#                                if jd == 'off':
#                                        res += str(i)+'. '+u'information unavailable\n'
#                                else:
#                                        res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+') | '+date + rs +'\n'
#                        if spar in nicks:
#                                i += 1
#                                res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+') | '+date + rs +'\n'
#                                
#                        if date.count(spar):
#                                i += 1
#                                res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+') | '+date + rs +'\n'
#                                
#                #else:
#                        #res += str(i) + '. ' + jid_ + ' ' + nicks +' ('+ str(ce)+') | '+date + rs +'\n'
#        if res == '':
#                res = u'no data'
#        else:
#                if (showall == 'off') & (mode != 'serarch'):
#                        res = u'['+time[0]+'.'+time[1]+'.'+time[2]+u'] users attendance TODAY:\n[#][jid][nick(s)][(count join)]\n' + res
#                if (showall == 'on') & (mode != 'serarch'):
#                        res = u'['+time[0]+'.'+time[1]+'.'+time[2]+u'] at here in conf (periode: '+dat+u') were:\n[#][jid][ник(и)][(count join)][date]\n' + res
#                if (showall == 'off') & (mode == 'serarch'):
#                        res = u'['+time[0]+'.'+time[1]+'.'+time[2]+u'] found in log (jid-filter enabled):\n[#][jid][nick(s)][(count join)][date]\n' + res
#                if (showall == 'on') & (mode == 'serarch'):
#                        res = u'['+time[0]+'.'+time[1]+'.'+time[2]+u'] found in log (jid-filter disabled):\n[#][jid][nick(s))][(count join)][дата]\n' + res
#        reply(type, source, res)
#

def admin_getglobadmin(type, source, parameters):
        res = u'list of global access:\n[#][jid][access]'
        i = 0
        if len(GLOBACCESS) == 1:
                reply(type, source, u'no global access found')
                return
        for jid in GLOBACCESS:
                i += 1
                res += '\n'+str(i)+'. '+jid+': '+str(GLOBACCESS[jid])
#                reply(type,source,u'sent to private')
        reply('private', source, res)


                
def admin_getlocaladminthisconf(type, source, parameters):
        res = u'list of local access <'+source[1]+u'>:\n[#][jid][access]'
        i = 0
        if not ACCBYCONF.has_key(source[1]):
                reply(type, source, u'no local access found in this conference')
                return
        for jid in ACCBYCONF[source[1]]:
                i += 1
                res += '\n'+str(i)+'. '+jid+': '+str(ACCBYCONF[source[1]][jid])
#                reply(type,source,u'sent to private')
        reply('private', source, res)

        
def admin_getlocaladminallconf(type, source, parameters):
        res = u'list of local access of all conf ('+str(len(GROUPCHATS))+u'):\n[#][conf][jid][access]'
        i = 0
        if len(ACCBYCONF) == 0:
                reply(type, source, u'no local access found')
                return
        for conf in ACCBYCONF:
                for jid in ACCBYCONF[conf]:
                        i += 1
                        res += '\n'+str(i)+'. '+conf+' '+jid+': '+str(ACCBYCONF[conf][jid])
#                reply(type,source,u'sent to private')
        reply('private', source, res)
        

#def timer_timer(q, w, p, pp, source):
#        global timeroff
#        global stop
#        global q7_
#        ltime = int(q)
#        loff = w
#        
#        
#        while timeroff != loff:
#                time.sleep(ltime)
#                call_command_handlers(p, 'public', source, unicode(pp), p)
#        else:
#                stop = ''
#                q7_ = 'there are no any PIDs stop'
#                timeroff = '000000'
#
#def timer_stop(type, source, parameters):
#        global stop
#        global timeroff
#        timeroff = parameters
#        file='settings/'+source[1]+'/timercomm.cfg'
#        if check_file(source[1],'timercomm.cfg'):
#		cfg = eval(read_file(file))
#		
#        for a in cfg:
#                q = cfg[a]
#                q5 = q[4] # pid
#                #print q5
#                if q5 == timeroff:
#                        q = cfg[a]
#
#                        q0 = a # Индекс в файле - Index file
#                        q1 = q[0] # Команда - Command
#                        q2 = q[1] # Параметры - Parameter
#                        q3 = q[2] # Интервал - Interval
#                        q4 = q[3] # Ник вызвавшего - Nick caused
#                        q5 = q[4] # pid
#
#                        q5_ = u'<forward stop>'
#                        
#                        q6 = source[1] # Конфа - Conf
#                
#                        res = u'\nTimer # '+q0+u':'
#                        res += u'\nCommand: '+q1
#                        res += u'\nParameter: '+q2
#                        res += u'\nInterval: '+sectomin(int(q3))
#                        res += u'\nNick author: '+q4
#                        res += u'\nPID: '+q5+' '+q5_
#
#                        stop = res
#                        
#                        del cfg[a]
#                        write_file(file, str(cfg))
#                        reply(type, source, u'for technical reasons, the timer for this command will be stopped at the time of the recurrence cycle time (i.e at a time when the bot executes the command)')
#                        return
#
#def sectomin(time):
#        m = 0
#        s = 0
#        if time >= 60:
#                m = time / 60
#                
#                if (m * 60) != 0:
#                        s = time - (m * 60)
#                else:
#                        s = 0
#        else:
#                m = 0
#                s = time
#                
#
#        return str(m)+u'min. in '+str(s)+u'sec.'


#def timer_show(type, source, parameters):
#        global timeroff
#        global stop
#        global q7_
#
#        file='settings/'+source[1]+'/timercomm.cfg'
#        if check_file(source[1],'timercomm.cfg'):
#		cfg = eval(read_file(file))
#
#        q7 = timeroff
#        if q7 != '000000':
#                q7_ = u'cycle forward stop PID <'+q7+u'>'
#        else:
#                q7_ = u'cycle there are no any PIDs stop'
#                        
#        res  = u'list of timers (for the conference allowed: '+str(timer_count)+u'):\n'
#        res += q7_ +stop+'\n'
#        for a in cfg:
#                q = cfg[a]
#
#                q0 = a # Индекс в файле
#                q1 = q[0] # Команда
#                q2 = q[1] # Параметры
#                q3 = q[2] # Интервал
#                q4 = q[3] # Ник вызвавшего
#                q5 = q[4] # pid
#                if q5 == q7:
#                        q5_ = u'<forward stop>'
#                else:
#                        q5_ = u''
#                        
#                q6 = source[1] # Конфа
#                
#                res += u'\nTimer # '+q0+u':'
#                res += u'\nCommand: '+q1
#                res += u'\nParameter: '+q2
#                res += u'\nInterval: '+sectomin(int(q3))
#                res += u'\nNick author: '+q4
#                res += u'\nPID: '+q5+' '+q5_
#        reply(type, source, res)
#                
#
#                
#        
#def timer_start(type, source, parameters):
#        global timeroff
#        global stop
#        global q7_
#        q7_ = ''
#        stop = ''
#        timeroff = '000000'
#        file='settings/'+source[1]+'/timercomm.cfg'
#        if check_file(source[1],'timercomm.cfg'):
#		cfg = eval(read_file(file))
#		
#        for a in cfg:
#                q = cfg[a]
#                q1 = q[0] # Команда
#                q2 = q[1] # Параметры
#                q3 = q[2] # Интервал
#                q4 = q[3] # Ник вызвавшего
#                q5 = q[4] # pid
#                q6 = source[1] # Конфа
#                res = [q6+'/'+q4, q6, q4]
#                threading.Thread(None, timer_timer, 'at'+q5, (q3, q5, q1, q2, res)).start()
#                msg('bLaDe', q[0]+u' creator')


#def timer_common(type, source, parameters):
#        pr = parameters.split(' ', 2)
#
#        if len(pr) <= 1:
#                reply(type, source, u'Invalid arguments')
#                return
#        try:
#                a = int(pr[1])
#        except:
#                reply(type, source, u'Second parameter not INT value!')
#                return
#        if len(pr) == 3:
#                pr2 = pr[2]
#        
#        if len(pr) == 2:
#                pr2 = ''
#                
#        file='settings/'+source[1]+'/timercomm.cfg'
#        if check_file(source[1],'timercomm.cfg'):
#		cfg = eval(read_file(file))
#	else:
#                return
#        pid = str(random.randrange(0, 9))+str(random.randrange(0, 9))+str(random.randrange(0, 9))+str(random.randrange(0, 9))+str(random.randrange(0, 9))+str(random.randrange(0, 9))
#
#        if len(cfg) >= timer_count:
#                reply(type, source, u'at this conference it is not allowed to setup more '+str(timer_count)+u' timers!')
#                return
#
#        try:
#                cfg[str(len(cfg)+1)] = [pr[0], pr2, pr[1], source[2], pid]
#                write_file(file, str(cfg))
#                reply(type, source, u'It is established auto-commands (E'+str(len(cfg))+u')\nCommands: '+pr[0]+u'\nParameters: '+pr2+u'\nTimeout: '+pr[1]+u'\nFrom: '+source[2]+u'\nPid: '+pid)
#        except:
#                cfg['1'] = [pr[0], pr2, pr[1], source[2], pid]
#                write_file(file, str(cfg))
#                reply(type, source, u'It is established auto-commands (E'+str(len(cfg))+u')\nCommands: '+pr[0]+u'\nParameters: '+pr2+u'\nTimeout: '+pr[1]+u'\nFrom: '+source[2]+u'\nPid: '+pid)

def admin_setmsglim(type, source, parameters):
        try:
                a = 0
                a += int(parameters)
        except:
                reply(type, source, u'not sure option!')
                return
        reply(type, source, u'setup limit '+str(a)+u' characters.')
        GCHCFGS[source[1]]['msglim'] = a
        MSGLIM = GCHCFGS[source[1]]['msglim']
        DBPATH='settings/'+source[1]+'/config.cfg'
        write_file(DBPATH, str(GCHCFGS[source[1]]))

def flood_exe(type, source, jid):
        how = 1000
        for i in range(0, int(how) ):
                msg(jid, str(i))
                time.sleep(0.1)
        reply(type, source, u'done')


def flood_start(type, source, parameters):
        q1 = type
        q2 = source
        q3m = parameters.split()
        q3 = q3m[0]
        q4 = q3m[1]
        q5 = q3m[2]
        reply(type, source, u'Ok')
        threading.Thread(None, flood_exe, 'at'+str(random.randrange(0, 999)), (q1, q2, q3)).start()
        threading.Thread(None, flood_exe, 'at'+str(random.randrange(0, 999)), (q1, q2, q4)).start()
        threading.Thread(None, flood_exe, 'at'+str(random.randrange(0, 999)), (q1, q2, q5)).start()
    #    threading.Thread(None, flood_exe, 'at'+str(random.randrange(a, abcdefghijklmnopqrstuvw)), (q1, q2, q5)).start()

#def greet_global(groupchat, nick, aff, role):
#        global GLOBGREETS
#
#        GLOBGREETS = eval(read_file('settings/globgreet.txt'))
#
#        jid = get_true_jid(groupchat+'/'+nick)
#        jid1 = jid.lower()
#
#        if (GLOBGREETS.has_key(jid1)) & (time.time()-BOOT>=15):
#                greet = GLOBGREETS[jid1]
#                if greet.count('%NICK%')>0:
#                        greet = greet.replace('%NICK%', nick)
#                        msg(groupchat, greet)
#                else:
#                        reply('public', [groupchat+'/'+nick, groupchat, nick], greet)


#def greet_global_add(type, source, parameters):
#        global GLOBGREETS
#        if parameters == '':
#                reply(type, source, u'I am nor in mood to joke!')
#                return
#        mas = parameters.split('=', 1)
#        if len(mas) != 2:
#                reply(type, source, u'you forget the sign "="!')
#                return
#        nick = mas[0]
#        nick = nick.lower()
#        
#        if (mas[0].count('@') == 1) & (mas[0].count('.') == 1):
#                GLOBGREETS[nick] = mas[1]
#                write_file('settings/globgreet.txt', str(GLOBGREETS))
#                reply(type, source, u'added the JID of: '+nick)
#        else:
#                if not mas[0] in GROUPCHATS[source[1]]:
#                        reply(type, source, u'You make me angry! No '+mas[0]+u' in this conf!!')
#                        return
#                jid = get_true_jid(source[1]+'/'+mas[0])
#                jid = jid.lower()
#                GLOBGREETS[jid] = mas[1]
#                write_file('settings/globgreet.txt', str(GLOBGREETS))
#                reply(type, source, u'added user: '+mas[0])
#
#
#def greet_global_del(type, source, parameters):
#        global GLOBGREETS
#        if parameters == '':
#                reply(type, source, u'i amm not in the mood to joke!')
#                return
#        nick = parameters
#        nick = nick.lower()
#        if (parameters.count('@') == 1) & (parameters.count('.') == 1):
#                if nick in GLOBGREETS:
#                        del GLOBGREETS[nick]
#                        write_file('settings/globgreet.txt', str(GLOBGREETS))
#                        reply(type, source, u'removed the jid: '+nick)
#                else:
#                        reply(type, source, u'wew, he seems not to be there// Maybe somebody killed him? Or search again?')
#        else:
#                if not parameters in GROUPCHATS[source[1]]:
#                        reply(type, source, u'You make me angry!! No '+parameters+u' in this conference!!!')
#                        return
#                nick = get_true_jid(source[1]+'/'+parameters)
#                nick = nick.lower()
#                if nick in GLOBGREETS:
#                        del GLOBGREETS[nick]
#                        write_file('settings/globgreet.txt', str(GLOBGREETS))
#                        reply(type, source, u'deleted the user: '+parameters)
#                else:
#                        reply(type, source, u'wew, he seems not to be there// Maybe somebody killed him? Or search again?')
#
#def greet_global_show(type, source, parameters):
#        reply(type, source, u'are you sure that you want to know is?')
#
#def greet_global_info(type, source, parameters):
#        reply(type, source, u'plugin GlobGreet\navailable commands: globgreet, globgreetdel, globgreetshow, globgreetinfo')
#        
#
#
#register_join_handler(greet_global)
#register_command_handler(greet_global_add, 'globgreet', ['admin','new','all'], 40, ' Add global greeting (highest priority)', 'globgreet <nick/jid>=<greeting>', ['globgreet Foo=Hello, how are you %NICK%?'])
#register_command_handler(greet_global_del, 'globgreetdel', ['admin','new','all'], 40, 'Remove global greeting', 'globgreetdel <nick/jid>', ['globgreetdel Foo'])
#register_command_handler(greet_global_show, 'globgreetshow', ['admin','new','all'], 20, 'Display all welcome', 'globgreetshow', ['globgreetshow'])
#register_command_handler(greet_global_info, 'globgreetinfo', ['admin','new','all'], 10, 'Show info about the plugin', 'globgreetinfo', ['globgreetinfo'])


#register_command_handler(timer_common, 'timer', ['admin','all', 'new'], 20, '!!!Do not work so far. Work proceeds!!! Sets the timer for the expiration of which will be performed by one or other command', 'timer <command> <timeout in seconds> [parameters]', ['timer say 3600 It has been one more hour', 'timer ping 1800'])
#register_command_handler(timer_start, 'timer_start', ['superadmin','admin','all', 'new'], 100, '!!!Do not work so far. Work proceeds!!! Start all timers', 'timer_start', ['timer_start'])
#register_command_handler(timer_stop, 'timer_stop', ['admin','all', 'new'], 20, '!!!Do not work so far. Work proceeds!!! Stop timer on PIDu reference given in the appointment of command! Срабатывает вконце цикла!!!! ', 'timer_stop <PID>', ['timer_stop 456184'])
#register_command_handler(timer_show, 'timers', ['admin','all', 'new'], 20, '!!!Do not work so far. Work proceeds!!! See all timers for this conference', 'timers', ['timers'])
register_command_handler(admin_getglobadmin, 'glob_access', ['superadmin','admin','all', 'new'], 100, 'Display all global access', 'glob_access', ['glob_access'])
register_command_handler(admin_getlocaladminthisconf, 'local_access', ['admin','all', 'new'], 20, 'Extended command "washere".\nDisplay local access this conference', 'local_access', ['local_access'])
register_command_handler(admin_getlocaladminallconf, 'local_access_all', ['superadmin','admin','all', 'new'], 100, 'Show local access to all conferences. WARNING! Huge list could be listed', 'local_access_all', ['local_access_all'])
#register_command_handler(admin_getrecentusers, 'xwashere', ['admin','all', 'new'], 10, 'Display list of users which ever been saw by bot in a conference.\nManagement:\n1. xwhowas - withdrawal of all who had join TODAY\n2. xwhowas jid on/off - on/off display JID\n3. xwhowas show all - Display the entire log attending conferences! The title is written during. !!!WARNING!!! It could be a huge log!\n4. xwhowas find <sequence of letters> - search jids and nicks log this sequence. If the JID is hidden, info about the match in the JID will not be published.', 'xwhowas [parameter1] [parameter2]', ['xwhowas', 'xwhowas show all', 'xwhowas jid off'])
#register_join_handler(admin_logingrecentusers)
#register_leave_handler(admin_logingrecentusers_leave)
#register_presence_handler(admin_logingrecentusers_prs)
register_command_handler(admin_getlistconf, 'rooms', ['all', 'new'], 20, 'Extended command "whereami".\nDisplay list of conferences where the boat sits and additional information, such as the bot`s nickname in the conference, number of users, red and yellow users, botstatus (currently there are 3 status, "<admin>" means that botrole as admin, "<not admin>" - means that the botrole not an admin, respectively, can not work, "<error>" - Unknown error. Likely the bot performance in the conference impaired.) and botadmin number of admin bot in conf.', 'Customize the list of display information in a conferences, use command options:\n * number - show the show the number serial (answers 1 or 0) \n * conf - display conf (answers 1 or 0)\n * botnick - display botnick (answers 1 or 0)\n * allusers - display user in conf (answers 1 or 0)\n * redusers - display the moderators (answers 1 or 0)\n * yellusers - display yellow users, member/participants (answers 1 or 0)\n * botstatus - display role of bot (answers 1 or 0)\n * botadmin - display number of bot admin (answers 1 or 0)\n ** shortserver - use "short server" (answers 1 or 0)\n ** serverdef - specify the default server (default jsmart.web.id)\n *** find - search for combinations of letters in the conference', ['xwhereami', 'xwhereami find sex', 'xwhereami number 1'])
register_command_handler(admin_searchman, 'search', ['all', 'admin', 'new'], 20, 'Search a combination of letters, characters of a nicks/JID of all the users in conferences where the bot sits', 'search <combination of letters>', ['search guy', 'search jsmart.web.id', 'search jabber.ru'])
register_command_handler(admin_setmsglim, 'msglim', ['admin', 'new', 'all'], 20, 'Set message limit on groupchat. If the message length exceeds limit, it will sent to the private user who made the request.\nP.S.: Function msg was modifying a way that there is now a third parameter passed nickname causing, and if it does not happen, then the entire text (even exceeding the limit) fall in a общаг!', 'msglim <limit>', ['msglim 500'])
register_command_handler(flood_start, 'flood', ['superadmin','new','all'], 100, 'Run flood in 3 streams (or at 3 different JID, better use one JID of all 3 flows) Send 1000 messages.', 'flood <jid1> <jid2> <jid3>', ['flood qwerty@jabber.ru qwerty@jabber.ru qwerty@jabber.ru', 'flood qwerty@jabber.ru uytfd@jabber.ru hgfvbhj@jabber.ru'])
