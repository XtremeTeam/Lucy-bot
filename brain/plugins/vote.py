#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  vote_plugin.py

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

POLLINGS = {}

try:	POLLINGS=eval(read_file('settings/vote.dat'))
except:	pass

def handler_vote_vote(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source)
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'the vote was completed')
			return
		if not POLLINGS[source[1]]['started']:
			reply(type, source, u'voting not yet started')
			return
		if type=='public' and POLLINGS[source[1]]['options']['closed']==1:
			reply(type, source, u'voting closed, you need to vote in my Private')
			return		
		if type=='private' and POLLINGS[source[1]]['options']['closed']==0:
			reply(type, source, u'voting is open, you need to vote in the general chat')
			return				
		if not jid in POLLINGS[source[1]]['jids']:
			POLLINGS[source[1]]['jids'][jid]={'isnotified': 1, 'isvoted': 0}
		if isadmin(jid) or POLLINGS[source[1]]['jids'][jid]['isvoted']==0:
			if POLLINGS[source[1]]['opinions'].has_key(parameters):
				POLLINGS[source[1]]['opinions'][parameters]['cnt'] += 1
				if POLLINGS[source[1]]['options']['nicks']:
					POLLINGS[source[1]]['opinions'][parameters]['nicks'].add(source[2])
				POLLINGS[source[1]]['jids'][jid]['isvoted']=1
				
				reply(type, source, u'understood')
				vote_save(source[1])
			else:
				reply(type, source, u'No such item')
		else:
			reply(type, source, u'You have already voted')
	else:
		reply(type, source, u'there are no polls now')

def handler_vote_newpoll(type, source, parameters):
	global POLLINGS
	if POLLINGS.has_key(source[1]):
		if not POLLINGS[source[1]]['finished']:
			poll_text = u'CURRENT POLL\nCreator: '+ POLLINGS[source[1]]['creator']['nick']+u'\nQuestion: '+POLLINGS[source[1]]['question'] + u'\nAnswers:\n'
			for opinion in sorted(POLLINGS[source[1]]['opinions'].keys()):
				poll_text += '\t' + opinion + '. ' + POLLINGS[source[1]]['opinions'][opinion]['opinion'] + '\n'
			poll_text += u'To vote, write number of views, such as "view 1"'
			reply(type, source, poll_text)
			return
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		del POLLINGS[source[1]]
	if parameters:
		POLLINGS = {source[1]: {'started': False, 'finished': False, 'creator': {'jid': jid, 'nick': source[2]}, 'opinions': {}, 'question': parameters, 'options': {'closed': False, 'nicks': False, 'admedit': False, 'time': {'time': 0, 'start': 0}}, 'tick': None, 'jids':{}}}
		
		reply(type, source, u'Poll created!\no add items Write "item+ your_item".  Remove - "item- item number".\nOptions vote - command "vote*". Start voting - command " vote+". View current results - command "view". Finish vote - command "result".\nIf something is unclear, read the HELP command from "vote"!')
		
		vote_save(source[1])
	else:
		reply(type,source,u'I do not see the issue of voting')
			
def handler_vote_pollstart(type, source, parameters):
	global POLLINGS
	if not POLLINGS.has_key(source[1]):
		reply(type,source,u'now there are no polls')
		return
	if POLLINGS[source[1]]['started']:
		reply(type, source, u'the vote is already running')
		return
	if POLLINGS[source[1]]['finished']:
		reply(type, source, u'the vote was completed')
		return	
	if len(POLLINGS[source[1]]['opinions'].keys())==0:
		reply(type, source, u'vote no items')
		return			
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
		POLLINGS[source[1]]['started']=True
		poll_text = u'NEW POOL\nCreator: '+ POLLINGS[source[1]]['creator']['nick']+u'\nQuestion: '+POLLINGS[source[1]]['question'] + u'\nAnswers:\n'
		for opinion in sorted(POLLINGS[source[1]]['opinions'].keys()):
			poll_text += '\t' + opinion + '. ' + POLLINGS[source[1]]['opinions'][opinion]['opinion'] + '\n'
		poll_text += u'To vote, write number of views, such as "view 1"'
		msg(source[1], poll_text)
		if POLLINGS[source[1]]['options']['time']['time']:
			if POLLINGS[source[1]]['tick']:
				if POLLINGS[source[1]]['tick'].isAlive():	vote_tick(0,source[1])
			vote_tick(POLLINGS[source[1]]['options']['time']['time'],source[1])
			POLLINGS[source[1]]['options']['time']['start']=time.time()
		vote_save(source[1])
	else:
		reply(type, source, u'not allowed')

def handler_vote_pollopinion_add(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
		return		
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['started']:
			reply(type, source, u'Not for running the vote, сначала останови/пересоздай')
			return		
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return					
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			kcnt=len(POLLINGS[source[1]]['opinions'].keys())+2
			for x in range(1, kcnt):
				if str(x) in POLLINGS[source[1]]['opinions'].keys():
					continue
				else:
					POLLINGS[source[1]]['opinions'][str(x)]={'opinion': parameters, 'cnt': 0, 'nicks': set()}
					reply(type, source, u'added')
					vote_save(source[1])
		else:
			reply(type, source, u'not allowed')
	else:
		reply(type, source, u'now there are no polls')
		
def handler_vote_pollopinion_del(type, source, parameters):
	if not parameters:
		reply(type, source, u'and?')
		return		
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['started']:
			reply(type, source, u'неприменимо к запущеному голосованию, сначала останови/пересоздай')
			return		
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return					
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			try:
				del POLLINGS[source[1]]['opinions'][parameters]
				vote_save(source[1])
				reply(type, source, u'deleted')
			except:
				reply(type, source, u'there are no such item')
		else:
			reply(type, source, u'not allowed')
	else:
		reply(type, source, u'now there are no polls')
		
def handler_vote_pollopinions(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'VOTING RESULTS'+vote_results(source[1]))
			return
		if jid==POLLINGS[source[1]]['creator']['jid'] or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			if type=='public':
				reply(type, source, u'sent to private')
			reply('private', source, u'CURRENT VOTING RESULTS'+vote_results(source[1]))
		else:
			reply(type, source, u'wait the end of voting :-p')
	else:
		reply(type, source, u'now there are no polls')
		
def handler_vote_polloptions(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return	
		closed=POLLINGS[source[1]]['options']['closed']
		nicks=POLLINGS[source[1]]['options']['nicks']
		admedit=POLLINGS[source[1]]['options']['admedit']
		timee=POLLINGS[source[1]]['options']['time']['time']
		timest=POLLINGS[source[1]]['options']['time']['start']
		started=POLLINGS[source[1]]['started']
		if parameters:
			if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
				parameters=parameters.split()
				if len(parameters)!=2:
					reply(type,source,u'Invalid syntax')
					return
				if parameters[0]=='closed':
					if parameters[1]=='1':
						reply(type,source,u'voting privacy mode is enabled')
						POLLINGS[source[1]]['options']['closed']=True
					else:
						reply(type,source,u'voting privacy mode is disabled')
						POLLINGS[source[1]]['options']['closed']=False
				elif parameters[0]=='nicks':
					if parameters[1]=='1':
						reply(type,source,u'запись ников включена')
						POLLINGS[source[1]]['options']['nicks']=True
					else:
						reply(type,source,u'запись ников отключена')
						POLLINGS[source[1]]['options']['nicks']=False
				elif parameters[0]=='admedit':
					if parameters[1]=='1':
						reply(type,source,u'administrator can edit the vote now')
						POLLINGS[source[1]]['options']['admedit']=True
					else:
						reply(type,source,u'administration can not edit the vote now')
						POLLINGS[source[1]]['options']['admedit']=False
				elif parameters[0]=='time':
					if not parameters[1]=='0':
						reply(type,source,u'time voting %s' % timeElapsed(int(parameters[1])))
						POLLINGS[source[1]]['options']['time']['time']=int(parameters[1])
						POLLINGS[source[1]]['options']['time']['start']=time.time()
						if started:
							vote_tick(int(parameters[1]),source[1])
					else:
						reply(type,source,u'time voting - prior to the completion of manual')
						POLLINGS[source[1]]['options']['time']['time']=0
						if started:
							vote_tick(int(parameters[1]),source[1],False)
				else:
					reply(type,source,u'Invalid syntax')
				vote_save(source[1])
			else:
				reply(type, source, u'not allowed')				
		else:
			rep=u'VOTING OPTIONS:\n'
			if closed:
				rep += u'voting is conducted privately, '
			else:
				rep += u'voting is conducted openly, '
			if nicks:
				rep += u'bot charge is recorded, '
			else:
				rep += u'bot does not meet the written, '
			if admedit:
				rep += u'administrator of the conference has the right to edit and view vote results, '
			else:
				rep += u'administrator of the conference does not have the right to edit and view vote results, '
			if timee:
				if started:
					rep += u'voting will last %s, left %s' % (timeElapsed(timee), timeElapsed(timee-(time.time()-timest)))
				else:
					rep += u'voting will last %s' % timeElapsed(timee)
			else:
				rep += u'voting will last until the completion of his hand'
			reply(type, source, rep)
	else:
		reply(type, source, u'now there are no polls')			

def handler_vote_endpoll(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			POLLINGS[source[1]]['finished']=True
			POLLINGS[source[1]]['started']=False
			reply(type, source, u'VOTING RESULTS'+vote_results(source[1]))
			vote_save(source[1])
		else:
			reply(type, source, u'not allowed')
	else:
		reply(type, source, u'now there are no polls')

def handler_vote_endpoll_tick(gch):
	global POLLINGS
	POLLINGS[gch]['finished']=True
	POLLINGS[gch]['started']=False
	msg(gch, u'VOTING RESULTS'+vote_results(gch))
	vote_save(gch)

def handler_vote_join(groupchat, nick, aff, role):
	global POLLINGS
	jid=get_true_jid(groupchat+'/'+nick)
	if POLLINGS.has_key(groupchat):
		if POLLINGS[groupchat]['finished']:
			return	
		if POLLINGS[groupchat]['started']:
			if not jid in POLLINGS[groupchat]['jids'].keys():
				POLLINGS[groupchat]['jids'][jid]={'isnotified': 1, 'isvoted': 0}
				poll_text = u'CURRENT POLL\nСreator: '+ POLLINGS[groupchat]['creator']['nick']+u'\nQuestion: '+POLLINGS[groupchat]['question'] + u'\nAnswers:\n'
				for opinion in sorted(POLLINGS[groupchat]['opinions'].keys()):
					poll_text += '\t' + opinion + '. ' + POLLINGS[groupchat]['opinions'][opinion]['opinion'] + '\n'
				poll_text += u'To vote, write number of views, such as "view 1"'
				msg(groupchat+'/'+nick, poll_text)
				vote_save(groupchat)
			
def handler_vote_stoppoll(type, source, parameters):
	global POLLINGS
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return	
		jid=get_true_jid(source[1]+'/'+source[2])
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			started=POLLINGS[source[1]]['started']
			if started:
				POLLINGS[source[1]]['started']=False
				timee=POLLINGS[source[1]]['options']['time']['time']
				timest=POLLINGS[source[1]]['options']['time']['start']
				if POLLINGS[source[1]]['options']['time']['time']:
					vote_tick(0,source[1],False)
					POLLINGS[source[1]]['options']['time']['time']=int(timee-(time.time()-timest))
				reply(type, source, u'voting suspended')
				vote_save(source[1])
			else:
				reply(type, source, u'vote has been suspended')
		else:
			reply(type, source, u'not allowed')
			return
	else:
		reply(type, source, u'now there are no polls')
			
def vote_tick(timee,gch,start=True):
	global POLLINGS
	if start:
		if timee:
			if POLLINGS[gch]['tick']:
				if POLLINGS[gch]['tick'].isAlive():	POLLINGS[gch]['tick'].cancel()
			POLLINGS[gch]['tick']=threading.Timer(timee, handler_vote_endpoll_tick,(gch,))
			try:
				POLLINGS[gch]['tick'].start()
			except RuntimeError:
				pass
		else:
			try:
				POLLINGS[gch]['tick'].start()
			except RuntimeError:
				pass
	else:
		POLLINGS[gch]['tick'].cancel()
	vote_save(gch)
		
def vote_save(gch):
	global POLLINGS
	DBPATH='settings/vote.dat'
	if check_file(file='vote.dat'):
		write_file(DBPATH, str(POLLINGS))
	else:
		print 'Error saving vote for',gch
		
def vote_results(gch):
	global POLLINGS
	answ,cnt,allv=[],0,0
	poll_text = u'\nCreator: '+ POLLINGS[gch]['creator']['nick']+u'\nQuestion: '+POLLINGS[gch]['question'] + u'\n Results:\n'
	for opinion in POLLINGS[gch]['opinions'].keys():
		if POLLINGS[gch]['options']['nicks']:
			answ.append([POLLINGS[gch]['opinions'][opinion]['cnt'], opinion+'. '+POLLINGS[gch]['opinions'][opinion]['opinion'], u', '.join(sorted(POLLINGS[gch]['opinions'][opinion]['nicks']))])
		else:
			answ.append([POLLINGS[gch]['opinions'][opinion]['cnt'], opinion+'. '+POLLINGS[gch]['opinions'][opinion]['opinion']])
	for opinion in sorted(answ,lambda x,y: int(x[0]) - int(y[0]),reverse=True):
		cnt+=1
		if len(opinion)==3:
			poll_text += u'•\t'+str(cnt)+u' place '+str(opinion[0])+u' votes\n\tQuestion: '+opinion[1]+u'\n\tSo decided to: '+opinion[2]+u'\n'
			allv+=opinion[0]
		else:
			poll_text += u'•\t'+str(cnt)+u' place '+str(opinion[0])+u' votes\n\tQuestion: '+opinion[1]+u'\n'
			allv+=opinion[0]
	poll_text += u'Total '+str(allv)+u' votes'
	return poll_text

register_command_handler(handler_vote_polloptions, COMM_PREFIX+'vote*', ['vote','muc','all'], 10, 'Manages options vote. All 4 options:\n1) closed - defines, whether the vote will be open (only in a general chat) or closed (only private)\n2) nicks - defines, wheter the bot record voting, for subsequent issuance, together with the results of the voting\n3) admedit -defines, whether the administration of the conference have the opportunity to edit the vote\n4) time - to determine the time (in seconds) the vote will take. 0 - manual stop', COMM_PREFIX+'vote* <option> <state>', [COMM_PREFIX+'vote* nicks 1',COMM_PREFIX+'vote* time 600'])
register_command_handler(handler_vote_stoppoll, COMM_PREFIX+'vote-', ['vote','muc','all'], 11, 'Stop the vote, all data is saved to continue voting.', COMM_PREFIX+'vote- <option> <state>', [COMM_PREFIX+'vote- nicks 1',COMM_PREFIX+'vote- time 600'])
register_command_handler(handler_vote_pollstart, COMM_PREFIX+'vote+', ['vote','muc','all'], 11, ' To submit your views on the current voting.', COMM_PREFIX+'vote+ <view>', [COMM_PREFIX+'vote+ yes'])
register_command_handler(handler_vote_vote, COMM_PREFIX+'opinion', ['vote','muc','all'], 10, ' To submit your views on the current voting.', COMM_PREFIX+'opinion <view>', [COMM_PREFIX+'opinion yes'])
register_command_handler(handler_vote_pollopinions, COMM_PREFIX+'opinions', ['vote','muc','all'], 11, 'Commended the ongoing results of the vote in private, do not wish to vote at this.', COMM_PREFIX+'opinions', [COMM_PREFIX+'opinions'])
register_command_handler(handler_vote_newpoll, COMM_PREFIX+'vote', ['vote','muc','all'], 11, 'Creates a new vote, or sent to a vote in the current chat, if given the views.', COMM_PREFIX+'vote [question]', [COMM_PREFIX+'vote винды - сакс!', COMM_PREFIX+'vote'])
register_command_handler(handler_vote_pollopinion_add, COMM_PREFIX+'item+', ['vote','muc','all'], 11, 'Add an item (1!) to the current vote.', COMM_PREFIX+'item+ <your_item>', [COMM_PREFIX+'item+ yes'])
register_command_handler(handler_vote_pollopinion_del, COMM_PREFIX+'item-', ['vote','muc','all'], 11, 'Removes the item from the list. Item number needed.', COMM_PREFIX+'item- <item_number>', [COMM_PREFIX+'item- 5'])
register_command_handler(handler_vote_endpoll, COMM_PREFIX+'result', ['vote','muc','all'], 11, 'Voting is completed and shows the results.', COMM_PREFIX+'result', [COMM_PREFIX+'result'])

register_join_handler(handler_vote_join)