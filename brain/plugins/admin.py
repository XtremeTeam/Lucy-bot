#===islucyplugin===
# -*- coding: utf-8 -*-


#  admin_plugin.py


#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def popups_check(gch):
	DBPATH='settings/'+gch+'/config.cfg'
	if GCHCFGS[gch].has_key('popups'):
		if GCHCFGS[gch]['popups'] == 1:
			return 1
		else:
			return 0
	else:
		GCHCFGS[gch]['popups']=1
		write_file(DBPATH,str(GCHCFGS[gch]))
		return 1

def remote(type, source, parameters):	
	groupchat = source[1]
	nick = source[2]
	
	groupchats = GROUPCHATS.keys()
	groupchats.sort()

	if parameters:
		spltdp = parameters.split(' ', 2)
		dest_gch = spltdp[0]
		
		if len(spltdp) >= 2:
			dest_comm = spltdp[1]
		else:
			reply(type, source, u'Invalid syntax!')
			return
		
		dest_params = ''
		
		if dest_gch.isdigit():
			if int(dest_gch) <= len(groupchats) and int(dest_gch) != 0:
				dest_gch = groupchats[int(dest_gch)-1]
			else:
				reply(type, source, u'The Conference does not exist!')
				return
		else:
			if not dest_gch in groupchats:
				reply(type, source, u'The Conference does not exist!')
				return
				
		if len(spltdp) >= 3:
			dest_params = spltdp[2]
		
		bot_nick = get_bot_nick(dest_gch)
		
		dest_source = [groupchat+'/'+nick,dest_gch,bot_nick]
		
		if COMMAND_HANDLERS.has_key(dest_comm.lower()):
			comm_hnd = COMMAND_HANDLERS[dest_comm.lower()]
		elif MACROS.macrolist[dest_gch].has_key(dest_comm.lower()):
			exp_alias = MACROS.expand(dest_comm.lower(), dest_source)
			
			spl_comm_par = exp_alias.split(' ',1)
			dest_comm = spl_comm_par[0]
			
			if len(spl_comm_par) >= 2:
				alias_par = spl_comm_par[1]
				dest_params = alias_par+' '+dest_params
				dest_params = dest_params.strip()
			
			if COMMAND_HANDLERS.has_key(dest_comm.lower()):
				comm_hnd = COMMAND_HANDLERS[dest_comm.lower()]
			else:
				reply(type, source, u'Unknown command!')
				return
		elif MACROS.gmacrolist.has_key(dest_comm.lower()):
			exp_alias = MACROS.expand(dest_comm.lower(), dest_source)
			
			spl_comm_par = exp_alias.split(' ',1)
			dest_comm = spl_comm_par[0]
			
			if len(spl_comm_par) >= 2:
				alias_par = spl_comm_par[1]
				dest_params = alias_par+' '+dest_params
				dest_params = dest_params.strip()
			
			if COMMAND_HANDLERS.has_key(dest_comm.lower()):
				comm_hnd = COMMAND_HANDLERS[dest_comm.lower()]
			else:
				reply(type, source, u'Unknown command!')
				return
		else:
			reply(type, source, u'Unknown command!')
			return
		
		if type == 'public':
			reply(type, source, u'Look in private!')
			
		comm_hnd('private',dest_source,dest_params)
	else:
		gchli = [u'%s) %s' % (groupchats.index(li)+1,li) for li in groupchats]
		
		if gchli:
			rep = u'Available Conferences:\n%s' % ('\n'.join(gchli))
		else:
			rep = u'No available conferences!'
			
		reply(type, source, rep)

def redirect(type, source, parameters):	
	groupchat = source[1]
	nick = source[2]
	
	if parameters:
		if ':' in parameters:
			spltdp = parameters.split(':', 1)
			dest_nick = spltdp[0]
			
			if len(spltdp) >= 2:
				mess = spltdp[1]
				comm_par = spltdp[1].strip()
				comm_par = comm_par.split(' ',1)
				comm = comm_par[0].strip()
				params = ''
				
				if len(comm_par) >= 2:
					params = comm_par[1].strip()
			else:
				reply(type, source, u'Invalid syntax!')
				return
			
			bot_nick = get_bot_nick(groupchat)
			
			dest_source = [groupchat+'/'+dest_nick,groupchat,bot_nick]
			
			if COMMAND_HANDLERS.has_key(comm.lower()):
				comm_hnd = COMMAND_HANDLERS[comm.lower()]
			elif MACROS.macrolist[groupchat].has_key(comm.lower()):
				exp_alias = MACROS.expand(comm.lower(), dest_source)
				
				spl_comm_par = exp_alias.split(' ',1)
				comm = spl_comm_par[0]
				
				if len(spl_comm_par) >= 2:
					alias_par = spl_comm_par[1]
					params = alias_par+' '+params
					params = params.strip()
				
				if COMMAND_HANDLERS.has_key(comm.lower()):
					comm_hnd = COMMAND_HANDLERS[comm.lower()]
				else:
					reply(type, source, u'Sent!')
					reply('private', [groupchat+'/'+dest_nick,groupchat,dest_nick], mess)
					return
			elif MACROS.gmacrolist.has_key(comm.lower()):
				exp_alias = MACROS.expand(comm.lower(), dest_source)
				
				spl_comm_par = exp_alias.split(' ',1)
				comm = spl_comm_par[0]
				
				if len(spl_comm_par) >= 2:
					alias_par = spl_comm_par[1]
					params = alias_par+' '+params
					params = params.strip()
				
				if COMMAND_HANDLERS.has_key(comm.lower()):
					comm_hnd = COMMAND_HANDLERS[comm.lower()]
				else:
					reply('private', [groupchat+'/'+dest_nick,groupchat,dest_nick], mess)
					reply(type, source, u'Sent!')
					return
			else:
				reply('private', [groupchat+'/'+dest_nick,groupchat,dest_nick], mess)
				reply(type, source, u'Sent!')
				return
			
			comm_hnd('private',dest_source,params)
			reply(type, source, u'Sent!')
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reply(type, source, u'Invalid syntax!')
	
def set_nick(type, source, parameters):
	if parameters:
		groupchat=source[1]
		nick=parameters
		join_groupchat(groupchat,nick)
		reply(type, source, u'Memorized!')
	else:
		reply(type, source, u'Read help on command!')
					
def lucy_join(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		passw=''
		args = parameters.split()
		if not args[0].count('@') or not args[0].count('.')>=1:
			reply(type, source, u'Read help on command!')
			return
		if len(args)>1:
			groupchat = args[0]
			passw = string.split(args[1], 'pass=', 1)
			if not passw[0]:
				bot_nick = ' '.join(args[2:])
			else:
				bot_nick = ' '.join(args[1:])
		else:
			groupchat = parameters
			bot_nick = ''
		get_gch_cfg(groupchat)
		for process in STAGE1_INIT:
			with smph:
				INFO['thr'] += 1
				try:
					threading.Thread(None,process,'atjoin_init'+str(INFO['thr']),(groupchat,)).start()
				except RuntimeError:
					pass
		DBPATH='settings/'+groupchat+'/config.cfg'
		write_file(DBPATH, str(GCHCFGS[groupchat]))
		if not passw:
			if not bot_nick:
				join_groupchat(groupchat, DEFAULT_NICK)
			else:
				join_groupchat(groupchat, bot_nick)
		else:
			if not bot_nick:
				join_groupchat(groupchat, DEFAULT_NICK, passw)
			else:
				join_groupchat(groupchat, bot_nick, passw)
		MACROS.load(groupchat)
		if bot_nick:
			reply(type, source, u'I have joined' + groupchat+u' with the nickname '+bot_nick+'.')
		else:
			reply(type, source, u'I have joined' + groupchat+u' with the nickname '+DEFAULT_NICK+'.')
		if popups_check(groupchat):
			msg(groupchat, u'joined by '+source[2]+'.')
	else:
		reply(type, source, u'Read help!')

def lucy_leave(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	args = parameters.split()
	if len(args)>1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'You do not have admin rights!')
			return
		reason = ' '.join(args[1:]).strip()
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'I am not there!')
			return
		groupchat = args[0]
	elif len(args)==1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'You do not have admin rights!')
			return
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'i am not there!')
			return
		reason = ''
		groupchat = args[0]
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'This command only possible in the conference!')
			return
		groupchat = source[1]
		reason = ''
	if popups_check(groupchat):
		if reason:
			msg(groupchat, u'I have left that conference. By '+source[2]+u' with reason:\n'+reason)
		else:
			msg(groupchat, u'I have left that conference. By '+source[2]+'.')
	if reason:
		leave_groupchat(groupchat, u'I have left that conference. By '+source[2]+u' with reason:\n'+reason)
	else:
		leave_groupchat(groupchat,u'I have left that conference. By '+source[2]+'.')
	reply(type, source, u'leaved ' + groupchat+'.')


def admin_msg(type, source, parameters):
	if not parameters:
		reply(type, source, u'Read help on the command!')
		return
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'Message sent!')
	
def glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'News from '+source[2]+u':\n'+parameters+u'\nI remind that as usual all a help can be got writing with "%shelp".\nAbout all of bugs, errors, suggestions and structural criticism, please to send me: write "%stell botadmin <text_message>", naturally without quotation marks.\nTHANKS FOR YOUR ATTENTION!')
				
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'Message sent to '+str(totalblock)+' conferences (from '+str(total)+').')
	else:
		reply(type, source, u'Read help on the command!')
		
def glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'News from '+source[2]+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'Message sent to '+str(totalblock)+' conferences (from '+str(total)+').')
	else:
		reply(type, source, u'Read help on the command!')

## This is commented out for a reason! ##		
#def handler_admin_say(type, source, parameters):
#	if parameters:
#		args=parameters.split()[0]
#		msg(source[1], parameters)
#	else:
#		reply(type, source, u'Read help on the command!')

def lucy_reload(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
	gch=[]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'restarted by '+source[2]+u' with reason:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'restarted by '+source[2]+'.')
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': restarted me --> '+reason)
	else:
		prs.setStatus(source[2]+u': restarted.')
	JCON.send(prs)
	time.sleep(1)
	JCON.disconnect()

def lucy_shdwn(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
	gch=[]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'shut down by '+source[2]+u' with reason:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'shut down by '+source[2]+'.')
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': shut me down --> '+reason)
	else:
		prs.setStatus(source[2]+u': shut me down.')
	JCON.send(prs)
	time.sleep(2)
	os.abort()
	
def popups_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'This command only possible in the conference!')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'Read help on the command!')
			return		
		DBPATH='settings/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['popups']=1
			reply(type,source,u'global notifications are turned on!')
		else:
			GCHCFGS[source[1]]['popups']=0
			reply(type,source,u'global notifications are turned off!')
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['popups']
		if ison==1:
			reply(type,source,u'global notifications are turned on here!')
		else:
			reply(type,source,u'global notifications are turned off here!')
			
def autoaway_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'This command only possible in the conference!')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'Read help on the command!')
			return		
		DBPATH='settings/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['autoaway']=1
			reply(type,source,u'auto-status enabled!')
		else:
			GCHCFGS[source[1]]['autoaway']=0
			reply(type,source,u'auto-status disabled!')
		get_autoaway_state(source[1])
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['autoaway']
		if ison==1:
			reply(type,source,u'auto-status is enable here!')
		else:
			reply(type,source,u'auto-status is disable here!')	
"""	
def handler_changebotstatus(type, source, parameters):
	if parameters:
		args,show,status=parameters.split(' ',1),'',''
		if args[0] in ['away','xa','dnd','chat']:
			show=args[0]
		else:
			show=None
			status=parameters
		if not status:
			try:
				status=args[1]
			except:
				status=None
		change_bot_status(source[1],status,show,0)
		GCHCFGS[source[1]]['status']={'status': status, 'show': show}
		reply(type,source, u'Status set.')
	else:
		stmsg=GROUPCHATS[source[1]][get_bot_nick(source[1])]['stmsg']
		status=GROUPCHATS[source[1]][get_bot_nick(source[1])]['status']
		if stmsg:
			reply(type,source, u'I am now '+status+u' ('+stmsg+u').')
		else:
			reply(type,source, u'I am now '+status+'.')
"""
def change_status(type, source, parameters):
   statusdict={u"xa":u"xa",u"dnd":u"dnd",u"online":u"online",u"away":u"away",u"chat":u"chat"}

   print source
   if check_file(file='statuses.list'):
     groupchatstatus = eval(read_file(GROUPCHAT_STATUS_CACHE_FILE))
     if parameters:      
       #if the status was recorded in the list, then bot will use it
       if groupchatstatus.has_key(source[1]):
         cstatus=groupchatstatus[source[1]]
       else: #otherwise bot will use the standard default settings
         cstatus=["online",None]

       sts=parameters.split(' ')
       if statusdict.has_key(sts[0].lower()):
         cstatus[0]=statusdict[sts[0].lower()]
         if sts[1:]!= []:
           cstatus[1]=" ".join(sts[1:])
       else:
         cstatus[1]=parameters

       groupchatstatus[source[1]]=cstatus
     else:
       del groupchatstatus[source[1]]
     write_file(GROUPCHAT_STATUS_CACHE_FILE,str(groupchatstatus))
   else: 
     print 'Error: unable to create chatrooms status list file!'

   if check_file(file='chatrooms.list'):
     lgcts = eval(read_file(GROUPCHAT_CACHE_FILE))
     gc=lgcts[source[1]]
     join_groupchat(source[1],gc["nick"],gc["passw"])
   else:
     print 'Error: unable to create chatrooms list file!'
			
def autoaway_state(gch):
	if not 'autoaway' in GCHCFGS[gch]:
		GCHCFGS[gch]['autoaway']=0
	if GCHCFGS[gch]['autoaway']:
		LAST['gch'][gch]['autoaway']=1
		LAST['gch'][gch]['thr']=None
"""		
def set_default_gch_status(gch):
	if isinstance(GCHCFGS[gch].get('status'), str): #temp workaround
		GCHCFGS[gch]['status']={'status': u'write "%shelp" and follow the instructions to understand how to work with me!' % (), 'show': u''}
	elif not isinstance(GCHCFGS[gch].get('status'), dict):
		GCHCFGS[gch]['status']={'status': u'write "%shelp" and follow the instructions to understand how to work with me!' % (), 'show': u''}
"""
def delivery(type,source,body):
	sender_jid = source[1]
	
	if GROUPCHATS.has_key(sender_jid):
		return
		
	if ADMINS_DELIVERY:
		if not sender_jid in ADMINS:
			prob_comm = body.split()[0].lower()
			cname = ''
			
			if sender_jid in ROSTER.getItems():
				subs = ROSTER.getSubscription(sender_jid)
				cname = ROSTER.getName(sender_jid)				
				#if subs != 'both':
				#	return
			#else:
			#	return
			
			if not cname:
				cname = sender_jid
			
			if not prob_comm in COMMANDS and not prob_comm in MACROS.gmacrolist:
				if cname != sender_jid:
					rep = u'Note from %s (%s):\n\n%s' % (cname, sender_jid, body)
				else:
					rep = u'Note from %s:\n\n%s' % (cname, body)
				
				for adli in ADMINS:
					msg(adli,rep)

				
register_command_handler(lucy_join, 'join', ['superadmin','muc','all','*'], 0, 'Join to a conference, if there is a password write that password right after the name of conference.', 'join <conference> [pass=1234] [botnick]', ['join botzone@conference.jabberuk.dyndns.org', 'join join botzone@conference.jsmart.web.id somebot', 'join join botzone@conference.jsmart.web.id pass=1234 somebot'])
register_command_handler(lucy_leave, 'leave', ['admin','muc','all','*'], 40, 'Leave bot from the current or a specific conference.', 'leave <conference> [reason]', ['leave botzone@conference.jabberuk.dyndns.org (reason = sleep', 'leave sleep','leave'])
register_command_handler(admin_msg, 'amsg', ['admin','muc','all','*'], 40, 'Send message on behalf of bot to a certain JID.', 'message <jid> <message>', ['message guy@jsmart.web.id how are you?'])
#register_command_handler(admin_say, 'say', ['admin','muc','all','*'], 20, 'Talk through bot.', 'say <message>', ['say *HI* peoples'])
register_command_handler(lucy_reload , 'reboot', ['superadmin','all','*'], 100, 'Restart bot.', 'restart [reason]', ['restart','restart refreshing!'])
register_command_handler(lucy_shdwn, 'shutd', ['superadmin','all','*'], 100, 'Shuts the bot down.', 'halt [reason]', ['halt','halt fixing bug!'])
register_command_handler(glob_msg, 'globmsg', ['superadmin','muc','all','*'], 100, 'Send message to all conference, where the bot exist.', 'globmsg [message]', ['globmsg hi all!'])
register_command_handler(glob_msg_help, 'hglobmsg', ['superadmin','muc','all','*'], 100, 'Send message to all conference, where the bot exist. The message will contain a header with a short pre help.', 'hglobmsg [message]', ['hglobmsg hi all!'])
register_command_handler(popups_onoff, 'popups', ['admin','muc','all','*'], 30, 'Off (0) and On (1) message about join/leaves, restarts/off, and also global news for certain conf. Without a parameter the bot will based on current state.', 'popups [1|0]', ['popups 1','popups'])
#register_command_handler(handler_botautoaway_onoff, 'autoaway', ['admin','muc','all','*'], 30, 'Off (0) and On (1) auto-status away due to abscence of commands within 10 minutes, without an option it will show current status.', 'autoaway [1|0]', ['autoaway 1','autoaway'])
register_command_handler(change_status, 'set_status', ['admin','muc','all','*'], 100, 'Change bot status in the current conference, if two parameters are not mentioned, bots will use the default status.', 'set_status [online|chat|away|xa|dnd] [message]', ['set_status away','set_status away go to work'])
register_command_handler(set_nick, 'rename', ['superadmin','muc','all','*'], 100, 'Changes the bot nickname in the current conference.', 'set_nick <nick>', ['set_nick somebot'])
register_command_handler(remote, 'remote', ['superadmin','muc','all','*'], 100, 'Allows you to remotely execute commands and aliases in other conferences on behalf of the bot and get the result. Without parameters displays a list of conferences with the numbers, instead of the full name of the conference can use a number from the list.', 'remote <groupchat|number from the list> <comm> <parameters>', ['remote botzone@conference.jsmart.web.id.aq ping guy','remote 2 time guy','remote'])
register_command_handler(redirect, 'redirect', ['admin','muc','all','*'], 20, 'Redirects the result of a command or an alias to the specified user in private. If the alias or command is not specified and instead the text, or any false, then sends the user a message.', 'redirect <nick>:<command>[<params>]|<mess>', ['redirect guy: ping lady'])

register_stage1_init(autoaway_state)
#register_stage1_init(set_default_gch_status)
register_message_handler(delivery)
#register_stage2_init(handler_admin_subscription)
