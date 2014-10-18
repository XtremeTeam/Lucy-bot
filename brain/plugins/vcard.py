#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  vcard_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications and New features Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

vcard_pending=[]

def get_novcard_state(gch):
	if not 'novcard' in GCHCFGS[gch]:
		GCHCFGS[gch]['novcard']={'res':'ignore','mess':u'Fill your vCard, so we know that you are not a spammer!\nAnd then come on in lets talk with pleasure! ;-)'}

def handler_vcardget(type, source, parameters):
	vcard_iq = xmpp.Iq('get')
	id='vcard'+str(random.randrange(1000, 9999))
	globals()['vcard_pending'].append(id)
	vcard_iq.setID(id)
	vcard_iq.addChild('vCard', {}, [], 'vcard-temp');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			nick = parameters.strip()
			if not nick in nicks:
				vcard_iq.setTo(nick)
			else:
				if GROUPCHATS[source[1]][nick]['ishere']==0:
					reply(type, source, u'Are you sure that user is here? :-O')
					return				
				jid=source[1]+'/'+nick
				vcard_iq.setTo(jid)
	else:
		jid=source[1]+'/'+source[2]
		vcard_iq.setTo(jid)
		nick=''
	JCON.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick})
		
def handler_vcardget_answ(coze, res, type, source, nick):
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'Ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
			if not nick:
				reply(type,source,u'Your Vcard is empty')
				return
			else:
				reply(type,source,u'That users Vcard is empty')
				return
		elif res.getType() == 'result':
			name,nickname,url,email,desc = '','','','',''
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:
				if not nick:
					reply(type,source,u'Fill in your vCard!')
					return
				else:
					reply(type,source,u'Tell them to fill in his vCard!')
					return
			for p in props:
				if p.getName() == 'NICKNAME':
					nickname = p.getData()
				if p.getName() == 'FN':
					name = p.getData()				
				if p.getName() == 'URL':
					url = p.getData()
				if p.getName() == 'EMAIL':
					email = p.getData()
				if p.getName() == 'DESC':
					desc = p.getData()
			if nickname:
				if not nick:
					rep = u'Here is your vCard:\nnick: '+nickname
				else:
					rep = u'Here is '+nick+u' vCard:\nnick: '+nickname
			if not name=='':
				rep +='\nName: '+name				
			if not url=='':
				rep +='\nURL: '+url
			if not email=='':
				rep +=u'\nE-mail: '+email		
			if not desc=='':
				rep +=u'\nAbout: '+desc
			if rep=='':
				rep = u'Empty vCard...'
		else:
			rep = u'He |-)'
	else:
		rep = u'Something in any way...'
	reply(type, source, rep)

def handler_novcard_join(groupchat, nick, aff, role):
	nvcres = GCHCFGS[groupchat]['novcard']['res']
	jid = groupchat+'/'+nick	
		
	type = 'public'
	source = [groupchat+'/'+nick,groupchat,nick]
		
	if aff == 'none' and nvcres != 'ignore':
		vcard_iq = xmpp.Iq('get')
		id='vcard'+str(random.randrange(1000, 9999))
		globals()['vcard_pending'].append(id)
		vcard_iq.setID(id)
		vcard_iq.addChild('vCard', {}, [], 'vcard-temp')
		vcard_iq.setTo(jid)
		JCON.SendAndCallForResponse(vcard_iq, handler_novcardget_answ, {'type': type, 'source': source, 'nick': nick})

def handler_novcardget_answ(coze, res, type, source, nick):
	groupchat = source[1]
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'Ooops!'
		return
	
	rep = 0
	nvcres = ''
	nvcmess = ''
	
	if res:
		if res.getType()=='error':
			nvcres = GCHCFGS[groupchat]['novcard']['res'].strip()
			nvcmess = GCHCFGS[groupchat]['novcard']['mess']
		elif res.getType() == 'result':
			name,nickname,url,email,desc,photo,adr,bday,gender,nn,org,tel = '','','','','',None,'','','','','',''
			props = None
			
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:	
				nvcres = GCHCFGS[groupchat]['novcard']['res'].strip()
				nvcmess = GCHCFGS[groupchat]['novcard']['mess']
			
			if not props:	
				nvcres = GCHCFGS[groupchat]['novcard']['res'].strip()
				nvcmess = GCHCFGS[groupchat]['novcard']['mess']
							
	if nvcres:
		if nvcres == 'kick':
			kick(groupchat, nick, nvcmess)
		elif nvcres == 'ban':
			ban(groupchat, nick, nvcmess)
		elif nvcres == 'visitor':
			visitor(groupchat, nick, nvcmess)
			msg(groupchat+'/'+nick,nvcmess)

def handler_novcard_res(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		if not parameters.strip() in ['ignore','kick','ban','visitor']:
			reply(type,source,u'Invalid syntax!')
			return
		
		GCHCFGS[groupchat]['novcard']['res']=parameters.strip()
		reply(type,source,u'the action of empty vCard will be '+parameters.strip()+'.')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		reply(type,source,u'The action of empty vCard will be: '+GCHCFGS[groupchat]['novcard']['res']+'.')
		
def handler_novcard_mess(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		GCHCFGS[groupchat]['novcard']['mess']=parameters.strip()
		reply(type,source,u'Message in response to the empty of vCard!')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		reply(type,source,u'Message in response to the empty of vCard: '+GCHCFGS[groupchat]['novcard']['mess'])

register_command_handler(handler_novcard_mess, 'novc_mess', ['muc','info','all','*'], 20, 'Sets or displays a message in reaction to an empty vCard.', 'novc_mess <message>', ['novc_mess Fill your vCard, then talk!','novc_mess'])
register_command_handler(handler_novcard_res, 'novc_res', ['muc','info','all','*'], 20, 'Sets or shows the reaction of a bot on an empty vCard.', 'novc_res [ignore|kick|ban|visitor]', ['novc_res kick','novc_res ban','novc_res'])
register_command_handler(handler_vcardget, 'vcard', ['muc','info','all','*'], 10, 'Displays the specified user vCard.', 'vcard [nick]', ['vcard guy','vcard'])

register_stage1_init(get_novcard_state)
register_join_handler(handler_novcard_join)